#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is a Python script written for scraping the website that stored the Toxics Release Inventory (TRI)
data. The TRI is the US Pollutant Release and Transfer Register (PRTR)
'''

# Importing libraries
from common import config

import os
import requests
import lxml.html as html
import re
import pandas as pd
import zipfile
import io
import csv

class TRIScrapper:

    def __init__(self):
        self._dir_path = os.path.dirname(os.path.realpath(__file__))
        self._config = config('config.yaml')['system']['TRI']
        self._queries = self._config['queries']
        self._url = self._config['url']


    def _visit(self):
        '''
        Method for visiting the TRI website that stores the historic record data
        '''

        regex = re.compile(r'https://.*/US_([0-9]{4}).zip')

        try:
            response = requests.get(self._url)
            if response.status_code == 200:
                home = response.content.decode('utf-8')
                parser = html.fromstring(home)
                links = parser.xpath(self._queries['options'])
                zip_urls = dict()
                for link in links:
                   year = re.search(regex, link).group(1)
                   zip_urls.update({year: link})
                return zip_urls
            else:
                raise ValueError(f'Error: {response.status_code}')
        except ValueError as ve:
            print(ve)
    

    def _calling_tri_columns(self):
        '''
        Method for calling column positions and names for TRI files 
        '''

        path_columns = os.path.join(self._dir_path, 'TRI_File_2a_columns.txt')
        columns = pd.read_csv(path_columns,
                              header=None)
        columns = columns[0].tolist()
        return columns            


    def extacting_tri_data_files(self):
        '''
        Method for extracting information for each TRI file by year
        '''

        # Calling the file sorted column names
        colum_names = self._calling_tri_columns()

        # Unzipping and organizing the TRI files
        zip_urls = self._visit()
        for year, zip_url in zip_urls.items():

            zip_file = requests.get(zip_url)
            raw_data_path = os.path.join(self._dir_path,
                                        os.pardir,
                                        os.pardir,
                                        'data',
                                        'raw')
            with zipfile.ZipFile(io.BytesIO(zip_file.content)) as z_file:
                z_file.extract(f'US_2a_{year}.txt' ,
                                raw_data_path)
                
            df = pd.read_csv(os.path.join(raw_data_path, f'US_2a_{year}.txt'),
                            header=None, encoding='ISO-8859-1',
                            error_bad_lines=False,
                            sep='\t', low_memory=True,
                            skiprows=[0], engine='python',
                            #lineterminator='\n',
                            usecols=range(len(colum_names)),
                            quoting=csv.QUOTE_NONE
                            )
            df.columns = colum_names
            df.to_csv(os.path.join(raw_data_path, f'US_2a_{year}.csv'),
                     sep=',', index=False)
            existing = False
            while not existing:
                existing = os.path.exists(os.path.join(raw_data_path, f'US_2a_{year}.csv'))
            os.remove(os.path.join(raw_data_path, f'US_2a_{year}.txt'))
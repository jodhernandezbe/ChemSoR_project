#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from common import config
from srs_scraper import get_cas_by_alternative_id
from nlm_scraper import looking_for_structure_details as nlm
from pubchem_scraper import looking_for_structure_details as pubchem

import os
import pandas as pd
import re


class TRITransformer:

    def __init__(self):
        self._dir_path = os.path.dirname(os.path.realpath(__file__))
        self._raw_data_path = os.path.join(self._dir_path,
                                        os.pardir,
                                        os.pardir,
                                        'data',
                                        'raw')
        self._transformed_data_path = os.path.join(self._dir_path,
                                        os.pardir,
                                        os.pardir,
                                        'data',
                                        'transformed')
        self._tri_columns = pd.read_csv(os.path.join(self._dir_path, 'columns_to_use.csv'))
        self._tables = config('database_schema.yaml')['tables']


    def _open_the_dataset_by_year(self, year):
        '''
        Method for opening the dataset year-by-year
        '''

        df_tri = pd.read_csv(os.path.join(self._raw_data_path, f'US_2a_{year}.csv'),
                            usecols=self._tri_columns['TRI_NAME'].to_list(),
                            low_memory=False)
        
        return df_tri

    def _looking_for_smiles(self, cas_number):
        '''
        Method to look for the SMILES using both the NLM and PubChem databases
        '''

        if cas_number:
            smiles = pubchem(cas_number)
            if not smiles:
                smiles = nlm(cas_number)

            return smiles
        else:
            return None

    
    def transforming_tri_datasets(self):
        '''
        Method for joind all year information and obtain database schema
        '''

        # Checking for all the 2a files available until now
        regex_year = re.compile(r'US_2a_([0-9]{4}).csv')
        tri_years = [re.search(regex_year, file).group(1)
                    for file in os.listdir(self._raw_data_path)
                    if re.match(regex_year, file)
                        ]

        # Checking the names
        names_for_change = {old_name: new_name
                                for old_name, new_name in zip(self._tri_columns['TRI_NAME'].tolist(),
                                                            self._tri_columns['DATABASE_NAME'].tolist()
                                                            )
                            }

        # Concatenating all the available years
        df_year_transformed = pd.DataFrame()
        for tri_year in tri_years:  

            df_year = self._open_the_dataset_by_year(tri_year)

            # Removing rows without useful information
            df_year = df_year[(pd.notnull(df_year['TRI_CHEM_ID'])) &
                            (~df_year['TRI_CHEM_ID'].str.startswith('N'))]
            df_year = df_year[pd.notnull(
                                    df_year[[col_name for col_name in df_year.columns if 'SOURCE REDUCTION ACTIVITY CODE' in col_name]]
                                        ).any(axis=1)
                             ]

            for i in range(4):
                df_aux = df_year[
                    [
                    'REPORTING YEAR', 'PRIMARY NAICS CODE', 'TRI_CHEM_ID',
                    'CHEMICAL NAME', 'CAAC_IND', 'CARC_IND', 'PFAS_IND', 'METAL_IND',
                    ] + df_year.columns[8 + 4*i: 8 + 4*(i + 1)].tolist()
                ]
                df_aux.rename(
                        columns=names_for_change,
                        inplace=True
                        )
                df_aux = df_aux[pd.notnull(df_aux['source_reduction_code'])]
                df_aux = df_aux[pd.notnull(df_aux['reduction_code'])]
                df_aux['source_reduction_description'] = df_aux['source_reduction_description'].str.capitalize()
                df_year_transformed = pd.concat([df_year_transformed, df_aux],
                                            axis=0, ignore_index=True)
                del df_aux

            del df_year

        # Creating and saving tables
        table_names = ['chemical', 'source_reduction_activity', 'reduction', 'record']
        for table_name in table_names:

            # Creating ids
            col_id = self._tables[table_name]['id']
            grouping = self._tables[table_name]['grouping']
            columns = self._tables[table_name]['columns']
            df_year_transformed[col_id] = pd.Series(df_year_transformed.groupby(grouping).ngroup() + 1)
            df_tables = df_year_transformed[columns].drop_duplicates(keep='first')

            if table_name == 'chemical':
                # Looking for cas numbers
                df_tables['cas_number'] = df_tables.apply(lambda x:
                                        get_cas_by_alternative_id(altId=x['tri_chemical_id'],
                                                                substanceName=x['chemical_name']),
                                            axis=1)

                # looking for SMILES
                df_tables['smiles'] = df_tables['cas_number'].apply(lambda cas: self._looking_for_smiles(cas))

            ## Saving table
            df_tables.to_csv(os.path.join(self._transformed_data_path,
                                         f'{table_name}.csv'),
                            index=False)


        


#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from base import creating_session_engine
from model import Chemical, Reduction, SourceReductionActivity, Record

import pandas as pd
import os

class TRILoader:

    def  __init__(self):

        self._engine, self._session = creating_session_engine()
        self._transformed_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                        os.pardir,
                                        os.pardir,
                                        'data',
                                        'transformed')


    def _opening_the_csv(self, table):
        '''
        Method for opening the csv file containing the table information
        '''

        table = pd.read_csv(os.path.join(self._transformed_data_path, f'{table}.csv'))

        return table
        

    def loading_data(self):
        '''
        Method to load the data into the database
        '''

        # Dictionary to associate each table file with each table in the SQL database
        Dic_tables = {'chemical': Chemical,
                    'reduction': Reduction,
                    'source_reduction_activity': SourceReductionActivity,
                    'record': Record}

        # Cleaning the tables
        for filename in reversed(list(Dic_tables.keys())):
            Object = Dic_tables[filename]
            Object.__table__.drop(self._engine, checkfirst=True)

        # Saving each table
        for filename, Object in Dic_tables.items():
            Object.__table__.create(self._engine, checkfirst=True)
            session = self._session()
            # Saving each record by table
            dfs = self._opening_the_csv(filename)
            for _, row in dfs.iterrows():
                context = row.to_dict()
                instance = Object(**context)
                session.add(instance)
            session.commit()
            session.close()
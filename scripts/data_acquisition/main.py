#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from extract import TRIScrapper
from transform import TRITransformer
from load import TRILoader

import logging

def data_acquisition_pipeline():
    '''
    Function to run the data acquisition pipeline (i.e., ETL)
    '''

    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger('Building the ChemSoR database')

    # Extracting
    logger.info(f' Extracting the TRI data')
    scrapper = TRIScrapper()
    scrapper.extacting_tri_data_files()

    # Transforming
    logger.info(f' Tranforming the TRI data')
    transformer = TRITransformer()
    transformer.transforming_tri_datasets()

    # Loading
    logger.info(f' Loading the TRI transformed data into the ChemSoR database')
    loader = TRILoader()
    loader.loading_data()


if __name__ == '__main__':

    data_acquisition_pipeline()
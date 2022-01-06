#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
import yaml
import os


def config(file_name):
    '''
    Description:
    Function to load the configuration file for scraping each PRTR website

    Input:
    file_name: string containing the name of .yaml file to open

    Output:
    __config: La información contenida en el archivo config.yaml como objeto python accesible por clave  
    '''

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, file_name),
                mode='r') as f:
        __config = yaml.load(f, Loader=yaml.FullLoader)

    return __config
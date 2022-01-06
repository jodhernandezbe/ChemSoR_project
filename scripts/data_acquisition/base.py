#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

def creating_session_engine(check_same_thread=True):
    '''
    Function to create SQLite session and engine
    '''

    dir_path = os.path.dirname(os.path.realpath(__file__)) # current directory path
    chemsor_path = os.path.join(dir_path,
                                os.pardir,
                                os.pardir,
                                'data',
                                'transformed',
                                'ChemSoR_database.db')

    Engine = create_engine(f'sqlite:///{chemsor_path}',
                        connect_args={"check_same_thread": check_same_thread})

    Session = sessionmaker(bind=Engine, autocommit=False, autoflush=False)

    return Engine, Session
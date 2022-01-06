#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from base import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Record(Base):
    __tablename__ = 'record'

    record_id = Column(Integer(), primary_key=True)
    reporting_year = Column(Integer(), nullable=False)
    naics_code = Column(Integer(), nullable=False)
    chemical_id = Column(Integer(),
                        ForeignKey(
                                'chemical.chemical_id',
                                ondelete='CASCADE',
                                onupdate='cascade'
                                ),
                        nullable=False)
    source_reduction_activity_id = Column(Integer(),
                                        ForeignKey(
                                            'source_reduction_activity.source_reduction_activity_id',
                                            ondelete='CASCADE',
                                            onupdate='cascade'
                                                ),
                                        nullable=False)
    reduction_id = Column(Integer(),
                        ForeignKey(
                            'reduction.reduction_id',
                            ondelete='CASCADE',
                            onupdate='cascade'
                                ),
                        nullable=False)

    source_reduction_activity = relationship("SourceReductionActivity", back_populates="records")
    reduction = relationship("Reduction", back_populates="records")
    chemical = relationship("Chemical", back_populates="records")

    def __init__(self, **kwargs):
        self.record_id = kwargs['record_id']
        self.reporting_year = kwargs['reporting_year']
        self.naics_code = kwargs['naics_code']
        self.chemical_id = kwargs['chemical_id']
        self.source_reduction_activity_id = kwargs['source_reduction_activity_id']
        self.reduction_id = kwargs['reduction_id']


class Chemical(Base):
    __tablename__ = 'chemical'

    chemical_id = Column(Integer(), primary_key=True)
    tri_chemical_id = Column(String(15), nullable=False)
    cas_number = Column(String(15), nullable=True)
    chemical_name = Column(String(200), nullable=False)
    caac_ind = Column(String(3), nullable=False)
    carc_ind = Column(String(3), nullable=False)
    pfas_ind = Column(String(3), nullable=False)
    metal_ind = Column(String(3), nullable=False)
    smiles = Column(String(600), nullable=True)
    
    records = relationship("Record", back_populates="chemical")

    def __init__(self, **kwargs):
        self.chemical_id = kwargs['chemical_id']
        self.tri_chemical_id = kwargs['tri_chemical_id']
        self.cas_number = kwargs['cas_number']
        self.chemical_name = kwargs['chemical_name']
        self.caac_ind = kwargs['caac_ind']
        self.carc_ind = kwargs['carc_ind']
        self.pfas_ind = kwargs['pfas_ind']
        self.metal_ind = kwargs['metal_ind']
        self.smiles = kwargs['smiles']


class Reduction(Base):
    __tablename__ = 'reduction'

    reduction_id = Column(Integer(), primary_key=True)
    reduction_code = Column(String(4), nullable=False)
    description_code = Column(String(50), nullable=False)

    records = relationship("Record", back_populates="reduction")

    def __init__(self, **kwargs):
        self.reduction_id = kwargs['reduction_id']
        self.reduction_code = kwargs['reduction_code']
        self.description_code = kwargs['description_code']


class SourceReductionActivity(Base):
    __tablename__ = 'source_reduction_activity'

    source_reduction_activity_id = Column(Integer(), primary_key=True)
    source_reduction_code = Column(String(4), nullable=False)
    source_reduction_description = Column(String(100), nullable=False)

    records = relationship("Record", back_populates="source_reduction_activity")

    def __init__(self, **kwargs):
        self.source_reduction_activity_id = kwargs['source_reduction_activity_id']
        self.source_reduction_code = kwargs['source_reduction_code']
        self.source_reduction_description = kwargs['source_reduction_description']
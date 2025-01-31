#!/usr/bin/python
""" Models for Applicant """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
from sqlalchemy.orm import relationship
import models
from marshmallow import Schema, fields
from datetime import datetime


class Applicant(BaseModel, Base):
    """
    Representation of Applicant.

    This class defines the Applicant model, which stores applicant information.

    Attributes:
        ApplicantID (int): Unique applicant ID.
        FullName (str): Full name of the applicant.
        Email (str): Email address of the applicant.
        PhoneNumber (str): Phone number of the applicant.
        DateOfBirth (date): Date of birth of the applicant.
        CreatedAt (datetime): Timestamp when the applicant was created.
        UpdatedAt (datetime): Timestamp when the applicant was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'Applicant'
        __table_args__ = {'schema': 'rdb_web_db'}

        ApplicantID = Column(Integer, primary_key=True, autoincrement=True,
                             doc="Unique applicant ID")
        FullName = Column(String(100), nullable=False,
                          doc="Full name of the applicant")
        Email = Column(String(100), unique=True, nullable=False,
                       doc="Email address of the applicant")
        PhoneNumber = Column(String(20), nullable=False,
                             doc="Phone number of the applicant")
        DateOfBirth = Column(Date, nullable=False,
                             doc="Date of birth of the applicant")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the applicant was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the applicant was last updated")

        # Relationships
        admissions = relationship('Admission', backref='applicant',
                                  doc="Admissions associated with this applicant")


class ApplicantSchema(Schema):
    ApplicantID = fields.Int(dump_only=True)
    FullName = fields.Str(required=True)
    Email = fields.Str(required=True)
    PhoneNumber = fields.Str(required=True)
    DateOfBirth = fields.Date(required=True)
    CreatedAt = fields.DateTime(dump_only=True)
    UpdatedAt = fields.DateTime(dump_only=True)

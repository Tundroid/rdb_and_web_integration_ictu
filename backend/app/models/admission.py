#!/usr/bin/python
""" Models for Applicant, Department, Program, Admission, and Notification """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
import models
from marshmallow import Schema, fields
from datetime import datetime


class Admission(BaseModel, Base):
    """
    Representation of Admission.

    This class defines the Admission model, which stores admission information.

    Attributes:
        AdmissionID (int): Unique admission ID.
        ApplicantID (int): Applicant ID (FK: Applicant.ApplicantID).
        ProgramCode (str): Program code (FK: Program.ProgramCode).
        ApplicationDate (date): Date of application.
        ApplicationStatus (str): Status of the application (Accepted, Pending, Rejected).
        CreatedAt (datetime): Timestamp when the admission was created.
        UpdatedAt (datetime): Timestamp when the admission was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'Admission'
        __table_args__ = {'schema': 'rdb_web_db'}

        AdmissionID = Column(Integer, primary_key=True, autoincrement=True,
                             doc="Unique admission ID")
        ApplicantID = Column(Integer, ForeignKey('rdb_web_db.Applicant.ApplicantID'),
                             nullable=False, doc="Applicant ID")
        ProgramCode = Column(String(10), ForeignKey('rdb_web_db.Program.ProgramCode'),
                             nullable=False, doc="Program code")
        ApplicationDate = Column(Date, nullable=False,
                                 doc="Date of application")
        ApplicationStatus = Column(Enum('Accepted', 'Pending', 'Rejected'),
                                   nullable=False, default='Pending',
                                   doc="Status of the application")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the admission was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the admission was last updated")

        # Relationships
        notifications = relationship('Notification', backref='admission',
                                     doc="Notifications associated with this admission")


class AdmissionSchema(Schema):
    AdmissionID = fields.Int(dump_only=True)
    ApplicantID = fields.Int(required=True)
    ProgramCode = fields.Str(required=True)
    ApplicationDate = fields.Date(required=True)
    ApplicationStatus = fields.Str(required=False)
    CreatedAt = fields.DateTime(dump_only=True)
    UpdatedAt = fields.DateTime(dump_only=True)

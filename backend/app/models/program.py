#!/usr/bin/python
""" Models for Applicant, Department, Program, Admission, and Notification """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
import models
from marshmallow import Schema, fields
from datetime import datetime


class Program(BaseModel, Base):
    """
    Representation of Program.

    This class defines the Program model, which stores program information.

    Attributes:
        ProgramCode (str): Unique program code.
        ProgramName (str): Name of the program.
        Duration (int): Duration of the program in months.
        DepartmentID (int): Department ID (FK: Department.DepartmentID).
        CreatedAt (datetime): Timestamp when the program was created.
        UpdatedAt (datetime): Timestamp when the program was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'Program'
        __table_args__ = {'schema': 'rdb_web_db'}

        ProgramCode = Column(String(10), primary_key=True,
                             doc="Unique program code")
        ProgramName = Column(String(100), unique=True, nullable=False,
                             doc="Name of the program")
        Duration = Column(Integer, nullable=False,
                          doc="Duration of the program in months")
        DepartmentID = Column(Integer, ForeignKey('rdb_web_db.Department.DepartmentID'),
                              nullable=False, doc="Department ID")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the program was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the program was last updated")

        # Relationships
        admissions = relationship('Admission', backref='program',
                                  doc="Admissions associated with this program")


class ProgramSchema(Schema):
    ProgramCode = fields.Str(required=True)
    ProgramName = fields.Str(required=True)
    Duration = fields.Int(required=True)
    DepartmentID = fields.Int(required=True)
    CreatedAt = fields.DateTime(dump_only=True)
    UpdatedAt = fields.DateTime(dump_only=True)

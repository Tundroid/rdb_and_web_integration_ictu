#!/usr/bin/python
""" Models for Applicant, Department, Program, Admission, and Notification """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
import models
from marshmallow import Schema, fields
from datetime import datetime


class Department(BaseModel, Base):
    """
    Representation of Department.

    This class defines the Department model, which stores department information.

    Attributes:
        DepartmentID (int): Unique department ID.
        DepartmentName (str): Name of the department.
        CreatedAt (datetime): Timestamp when the department was created.
        UpdatedAt (datetime): Timestamp when the department was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'Department'
        __table_args__ = {'schema': 'rdb_web_db'}

        DepartmentID = Column(Integer, primary_key=True, autoincrement=True,
                              doc="Unique department ID")
        DepartmentName = Column(String(100), nullable=False,
                                doc="Name of the department")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the department was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the department was last updated")

        # Relationships
        programs = relationship('Program', backref='department',
                                doc="Programs associated with this department")


class DepartmentSchema(Schema):
    DepartmentID = fields.Int(dump_only=True)
    DepartmentName = fields.Str(required=True)
    CreatedAt = fields.DateTime(dump_only=True)
    UpdatedAt = fields.DateTime(dump_only=True)

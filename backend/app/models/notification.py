#!/usr/bin/python
""" Models for Applicant, Department, Program, Admission, and Notification """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, Text, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
import models
from marshmallow import Schema, fields
from datetime import datetime


class Notification(BaseModel, Base):
    """
    Representation of Notification.

    This class defines the Notification model, which stores notification information.

    Attributes:
        NotificationID (int): Unique notification ID.
        AdmissionID (int): Admission ID (FK: Admission.AdmissionID).
        Message (str): Notification message.
        NotificationStatus (str): Status of the notification (Sent, Unsent).
        CreatedAt (datetime): Timestamp when the notification was created.
        UpdatedAt (datetime): Timestamp when the notification was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'Notification'
        __table_args__ = {'schema': 'rdb_web_db'}

        NotificationID = Column(Integer, primary_key=True, autoincrement=True,
                                doc="Unique notification ID")
        AdmissionID = Column(Integer, ForeignKey('rdb_web_db.Admission.AdmissionID'),
                             nullable=False, doc="Admission ID")
        Message = Column(Text, nullable=False,
                         doc="Notification message")
        NotificationStatus = Column(Enum('Sent', 'Unsent'),
                                   nullable=False, default='Unsent',
                                   doc="Status of the notification")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the notification was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the notification was last updated")


class NotificationSchema(Schema):
    NotificationID = fields.Int(dump_only=True)
    AdmissionID = fields.Int(required=True)
    Message = fields.Str(required=True)
    NotificationStatus = fields.Str(missing="Unsent")
    CreatedAt = fields.DateTime(dump_only=True)
    UpdatedAt = fields.DateTime(dump_only=True)
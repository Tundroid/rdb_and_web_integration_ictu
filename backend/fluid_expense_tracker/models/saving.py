#!/usr/bin/python
""" Saving class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, Date, Time, Text, TIMESTAMP
from sqlalchemy.orm import relationship
import models
from marshmallow import Schema, fields
from datetime import datetime


class Saving(BaseModel, Base):
    """
    Representation of Saving.

    This class defines the Saving model, which stores saving information.

    Attributes:
        SavingID (int): Unique saving ID.
        Amount (int): Saving amount.
        SavingDate (date): Saving date.
        SavingTime (Time): Saving time.
        SavingLocation (str): Saving location.
        SavingDescription (str): Saving description.
        SavingGoalID (int): Saving goal ID (FK: SavingGoal.SavingGoalID).
        UserID (int): User ID (FK: User.UserID).
        CreatedAt (datetime): Timestamp when the saving was created.
        UpdatedAt (datetime): Timestamp when the saving was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'Saving'
        __table_args__ = {'schema': 'fet_db'}

        SavingID = Column(Integer, primary_key=True, autoincrement=True,
                    doc="Unique saving ID")
        Amount = Column(Integer, nullable=False,
                          doc="Saving amount")
        SavingDate = Column(Date, nullable=False,
                      doc="Saving date")
        SavingTime = Column(Time, nullable=False,
                       doc="Saving time")
        SavingLocation = Column(Text,
                           doc="Saving location")
        SavingDescription = Column(Text,
                              doc="Saving description")
        SavingGoalID = Column(Integer, ForeignKey('fet_db.SavingGoal.SavingGoalID'),
                               doc="Saving goal ID")
        UserID = Column(Integer, ForeignKey('fet_db.User.UserID'), nullable=False,
                      doc="User ID")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the saving was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the saving was last updated")

        # Establish relationships
        user = relationship('User', backref='savings',
                            doc="User relationship")
        saving_goal = relationship('SavingGoal', backref='savings',
                                    doc="Saving goal relationship")


    def __init__(self, *args, **kwargs):
        """
        Saving initialization.

        Initializes the Saving object with the given arguments.
        """
        super().__init__(*args, **kwargs)


class SavingSchema(Schema):
    """
    Saving schema.

    This schema defines the structure of the Saving data.

    Attributes:
        SavingID (int): Unique saving ID.
        Amount (int): Saving amount.
        SavingDate (date): Saving date.
        SavingTime (time): Saving time.
        SavingLocation (str): Saving location.
        SavingDescription (str): Saving description.
        SavingGoalID (int): Saving goal ID.
        UserID (int): User ID.
        CreatedAt (datetime): Timestamp when the saving was created.
        UpdatedAt (datetime): Timestamp when the saving was last updated.
    """
    SavingID = fields.Int(required=False, doc="Unique saving ID")
    Amount = fields.Int(required=True, doc="Saving amount")
    SavingDate = fields.Date(required=True, doc="Saving date")
    SavingTime = fields.Time(required=True, doc="Saving time")
    SavingLocation = fields.Str(required=False, doc="Saving location")
    SavingDescription = fields.Str(required=False, doc="Saving description")
    SavingGoalID = fields.Int(required=False, doc="Saving goal ID")
    UserID = fields.Int(required=True, doc="User ID")
    CreatedAt = fields.DateTime(required=False, doc="Timestamp when the saving was created")
    UpdatedAt = fields.DateTime(required=False, doc="Timestamp when the saving was last updated")

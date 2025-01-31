#!/usr/bin/python
""" SavingGoal class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, Date, Text, TIMESTAMP
from sqlalchemy.orm import relationship
import models
from marshmallow import Schema, fields
from datetime import datetime


class SavingGoal(BaseModel, Base):
    """
    Representation of SavingGoal.

    This class defines the SavingGoal model, which stores saving goal information.

    Attributes:
        SavingGoalID (int): Unique saving goal ID.
        SavingGoalTarget (int): Saving goal target amount.
        DateLimit (date): Saving goal date limit.
        SavingGoalDescription (str): Saving goal description.
        UserID (int): User ID (FK: User.UserID).
        CreatedAt (datetime): Timestamp when the saving goal was created.
        UpdatedAt (datetime): Timestamp when the saving goal was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'SavingGoal'
        __table_args__ = {'schema': 'fet_db'}

        SavingGoalID = Column(Integer, primary_key=True, autoincrement=True,
                    doc="Unique saving goal ID")
        SavingGoalTarget = Column(Integer, nullable=False,
                          doc="Saving goal target amount")
        DateLimit = Column(Date, nullable=False,
                            doc="Saving goal date limit")
        SavingGoalDescription = Column(Text,
                              doc="Saving goal description")
        UserID = Column(Integer, ForeignKey('fet_db.User.UserID'), nullable=False,
                      doc="User ID")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the saving goal was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the saving goal was last updated")

        # Establish relationships
        user = relationship('User', backref='saving_goals',
                            doc="User relationship")


    def __init__(self, *args, **kwargs):
        """
        SavingGoal initialization.

        Initializes the SavingGoal object with the given arguments.
        """
        super().__init__(*args, **kwargs)


class SavingGoalSchema(Schema):
    """
    SavingGoal schema.

    This schema defines the structure of the SavingGoal data.

    Attributes:
        SavingGoalID (int): Unique saving goal ID.
        SavingGoalTarget (int): Saving goal target amount.
        DateLimit (date): Saving goal date limit.
        SavingGoalDescription (str): Saving goal description.
        UserID (int): User ID.
        CreatedAt (datetime): Timestamp when the saving goal was created.
        UpdatedAt (datetime): Timestamp when the saving goal was last updated.
    """
    SavingGoalID = fields.Int(required=False, doc="Unique saving goal ID")
    SavingGoalTarget = fields.Int(required=True, doc="Saving goal target amount")
    DateLimit = fields.Date(required=True, doc="Saving goal date limit")
    SavingGoalDescription = fields.Str(required=False, doc="Saving goal description")
    UserID = fields.Int(required=True, doc="User ID")
    CreatedAt = fields.DateTime(required=False, doc="Timestamp when the saving goal was created")
    UpdatedAt = fields.DateTime(required=False, doc="Timestamp when the saving goal was last updated")

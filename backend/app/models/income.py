#!/usr/bin/python
""" Income class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, Date, Time, Text, TIMESTAMP
from sqlalchemy.orm import relationship
import models
from marshmallow import Schema, fields
from datetime import datetime


class Income(BaseModel, Base):
    """
    Representation of Income.

    This class defines the Income model, which stores income information.

    Attributes:
        IncomeID (int): Unique income ID.
        Amount (int): Income amount.
        IncomeDate (date): Income date.
        IncomeTime (time): Income time.
        IncomeDescription (str): Income description.
        CategoryID (int): Category ID (FK: Category.CategoryID).
        UserID (int): User ID (FK: User.UserID).
        CreatedAt (datetime): Timestamp when the income was created.
        UpdatedAt (datetime): Timestamp when the income was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'Income'
        __table_args__ = {'schema': 'fet_db'}

        IncomeID = Column(Integer, primary_key=True, autoincrement=True,
                    doc="Unique income ID")
        Amount = Column(Integer, nullable=False,
                          doc="Income amount")
        IncomeDate = Column(Date, nullable=False,
                      doc="Income date")
        IncomeTime = Column(Time, nullable=False,
                       doc="Income time")
        IncomeDescription = Column(Text,
                              doc="Income description")
        CategoryID = Column(Integer, ForeignKey('fet_db.Category.CategoryID'), nullable=False,
                            doc="Category ID")
        UserID = Column(Integer, ForeignKey('fet_db.User.UserID'), nullable=False,
                      doc="User ID")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the income was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the income was last updated")

        # Establish relationships
        user = relationship('User', backref='incomes',
                            doc="User relationship")
        category = relationship('Category', backref='incomes',
                                 doc="Category relationship")


    def __init__(self, *args, **kwargs):
        """
        Income initialization.

        Initializes the Income object with the given arguments.
        """
        super().__init__(*args, **kwargs)


class IncomeSchema(Schema):
    """
    Income schema.

    This schema defines the structure of the Income data.

    Attributes:
        IncomeID (int): Unique income ID.
        Amount (int): Income amount.
        IncomeDate (date): Income date.
        IncomeTime (time): Income time.
        IncomeDescription (str): Income description.
        CategoryID (int): Category ID.
        UserID (int): User ID.
        CreatedAt (datetime): Timestamp when the income was created.
        UpdatedAt (datetime): Timestamp when the income was last updated.
    """
    IncomeID = fields.Int(required=False, doc="Unique income ID")
    Amount = fields.Int(required=True, doc="Income amount")
    IncomeDate = fields.Date(required=True, doc="Income date")
    IncomeTime = fields.Time(required=False, doc="Income time")
    IncomeDescription = fields.Str(required=False, doc="Income description")
    CategoryID = fields.Int(required=True, doc="Category ID")
    UserID = fields.Int(required=True, doc="User ID")
    CreatedAt = fields.DateTime(required=False, doc="Timestamp when the income was created")
    UpdatedAt = fields.DateTime(required=False, doc="Timestamp when the income was last updated")

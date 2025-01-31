#!/usr/bin/python
""" Budget class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, Date, Text, TIMESTAMP
from sqlalchemy.orm import relationship
import models
from marshmallow import Schema, fields
from datetime import datetime


class Budget(BaseModel, Base):
    """
    Representation of Budget.

    This class defines the Budget model, which stores budget information.

    Attributes:
        BudgetID (int): Unique budget ID.
        Amount (int): Budget amount.
        BudgetStart (date): Budget start date.
        BudgetEnd (date): Budget end date.
        BudgetDescription (str): Budget description.
        CategoryID (int): Category ID (FK: Category.CategoryID).
        UserID (int): User ID (FK: User.UserID).
        CreatedAt (datetime): Timestamp when the budget was created.
        UpdatedAt (datetime): Timestamp when the budget was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'Budget'
        __table_args__ = {'schema': 'fet_db'}

        BudgetID = Column(Integer, primary_key=True, autoincrement=True,
                    doc="Unique budget ID")
        Amount = Column(Integer, nullable=False,
                          doc="Budget amount")
        BudgetStart = Column(Date, nullable=False,
                        doc="Budget start date")
        BudgetEnd = Column(Date, nullable=False,
                      doc="Budget end date")
        BudgetDescription = Column(Text,
                              doc="Budget description")
        CategoryID = Column(Integer, ForeignKey('fet_db.Category.CategoryID'),
                            doc="Category ID")
        UserID = Column(Integer, ForeignKey('fet_db.User.UserID'), nullable=False,
                      doc="User ID")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the budget was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the budget was last updated")

        # Establish relationships
        user = relationship('User', backref='budgets',
                            doc="User relationship")
        category = relationship('Category', backref='budgets',
                                 doc="Category relationship")


    def __init__(self, *args, **kwargs):
        """
        Budget initialization.

        Initializes the Budget object with the given arguments.
        """
        super().__init__(*args, **kwargs)


class BudgetSchema(Schema):
    """
    Budget schema.

    This schema defines the structure of the Budget data.

    Attributes:
        BudgetID (int): Unique budget ID.
        Amount (int): Budget amount.
        BudgetStart (date): Budget start date.
        BudgetEnd (date): Budget end date.
        BudgetDescription (str): Budget description.
        CategoryID (int): Category ID.
        UserID (int): User ID.
        CreatedAt (datetime): Timestamp when the budget was created.
        UpdatedAt (datetime): Timestamp when the budget was last updated.
    """
    BudgetID = fields.Int(required=False, doc="Unique budget ID")
    Amount = fields.Int(required=True, doc="Budget amount")
    BudgetStart = fields.Date(required=True, doc="Budget start date")
    BudgetEnd = fields.Date(required=True, doc="Budget end date")
    Description = fields.Str(required=False, doc="Budget description")
    CategoryID = fields.Int(required=False, doc="Category ID")
    UserID = fields.Int(required=True, doc="User ID")
    CreatedAt = fields.DateTime(required=False, doc="Timestamp when the budget was created")
    UpdatedAt = fields.DateTime(required=False, doc="Timestamp when the budget was last updated")
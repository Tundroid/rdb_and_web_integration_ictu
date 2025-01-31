#!/usr/bin/python
""" Expense class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, Date, Time, Text, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
import models
from marshmallow import Schema, fields
from datetime import datetime


class Expense(BaseModel, Base):
    """
    Representation of Expense.

    This class defines the Expense model, which stores expense information.

    Attributes:
        ExpenseID (int): Unique expense ID.
        Amount (int): Expense amount.
        ExpenseDate (date): Expense date.
        ExpenseTime (time): Expense time.
        Recurring (bool): Whether the expense is recurring.
        ExpenseDescription (str): Expense description.
        BudgetID (int): Budget ID (FK: Budget.BudgetID).
        CategoryID (int): Category ID (FK: Category.CategoryID).
        UserID (int): User ID (FK: User.UserID).
        CreatedAt (datetime): Timestamp when the expense was created.
        UpdatedAt (datetime): Timestamp when the expense was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'Expense'
        __table_args__ = {'schema': 'fet_db'}

        ExpenseID = Column(Integer, primary_key=True, autoincrement=True,
                    doc="Unique expense ID")
        Amount = Column(Integer, nullable=False,
                          doc="Expense amount")
        ExpenseDate = Column(Date, nullable=False,
                      doc="Expense date")
        ExpenseTime = Column(Time, nullable=False,
                       doc="Expense time")
        Recurring = Column(Boolean, default=False,
                            doc="Whether the expense is recurring")
        ExpenseDescription = Column(Text,
                              doc="Expense description")
        BudgetID = Column(Integer, ForeignKey('fet_db.Budget.BudgetID'),
                          doc="Budget ID")
        CategoryID = Column(Integer, ForeignKey('fet_db.Category.CategoryID'), nullable=False,
                            doc="Category ID")
        UserID = Column(Integer, ForeignKey('fet_db.User.UserID'), nullable=False,
                      doc="User ID")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the expense was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the expense was last updated")

        # Establish relationships
        user = relationship('User', backref='expenses',
                            doc="User relationship")
        category = relationship('Category', backref='expenses',
                                 doc="Category relationship")
        budget = relationship('Budget', backref='expenses',
                               doc="Budget relationship")


    def __init__(self, *args, **kwargs):
        """
        Expense initialization.

        Initializes the Expense object with the given arguments.
        """
        super().__init__(*args, **kwargs)


class ExpenseSchema(Schema):
    """
    Expense schema.

    This schema defines the structure of the Expense data.

    Attributes:
        ExpenseID (int): Unique expense ID.
        Amount (int): Expense amount.
        ExpenseDate (date): Expense date.
        ExpenseTime (time): Expense time.
        Recurring (bool): Whether the expense is recurring.
        ExpenseDescription (str): Expense description.
        BudgetID (int): Budget ID.
        CategoryID (int): Category ID.
        UserID (int): User ID.
        CreatedAt (datetime): Timestamp when the expense was created.
        UpdatedAt (datetime): Timestamp when the expense was last updated.
    """
    ExpenseID = fields.Int(required=False, doc="Unique expense ID")
    Amount = fields.Int(required=True, doc="Expense amount")
    ExpenseDate = fields.Date(required=True, doc="Expense date")
    ExpenseTime = fields.Time(required=False, doc="Expense time")
    Recurring = fields.Bool(required=False, doc="Whether the expense is recurring")
    ExpenseDescription = fields.Str(required=False, doc="Expense description")
    BudgetID = fields.Int(required=False, doc="Budget ID")
    CategoryID = fields.Int(required=True, doc="Category ID")
    UserID = fields.Int(required=True, doc="User ID")
    CreatedAt = fields.DateTime(required=False, doc="Timestamp when the expense was created")
    UpdatedAt = fields.DateTime(required=False, doc="Timestamp when the expense was last updated")

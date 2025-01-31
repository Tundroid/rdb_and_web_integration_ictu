#!/usr/bin/python
""" Category class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
import models
from marshmallow import Schema, fields
from datetime import datetime


class Category(BaseModel, Base):
    """
    Representation of Category.

    This class defines the Category model, which stores category information.

    Attributes:
        CategoryID (int): Unique category ID.
        CategoryName (str): Category name.
        CategoryType (str): Category type (Expense or Income).
        UserID (int): User ID (FK: User.UserID).
        CreatedAt (datetime): Timestamp when the category was created.
        UpdatedAt (datetime): Timestamp when the category was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'Category'
        __table_args__ = {'schema': 'fet_db'}

        CategoryID = Column(Integer, primary_key=True, autoincrement=True,
                    doc="Unique category ID")
        CategoryName = Column(String(100), nullable=False,
                          doc="Category name")
        UserID = Column(Integer, ForeignKey('fet_db.User.UserID'), nullable=False,
                      doc="User ID")
        CategoryType = Column(Enum('Budget', 'Expense', 'Income', 'Saving'), nullable=False,
                      doc="Category type (Expense or Income)")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the category was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the category was last updated")

        # Establish relationships
        user = relationship('User', backref='categories',
                            doc="User relationship")
        

    def __init__(self, *args, **kwargs):
        """
        Category initialization.

        Initializes the Category object with the given arguments.
        """
        super().__init__(*args, **kwargs)


class CategorySchema(Schema):
    """
    Category schema.

    This schema defines the structure of the Category data.

    Attributes:
        CategoryID (int): Unique category ID.
        CategoryName (str): Category name.
        CategoryType (str): Category type (Expense or Income).
        UserID (int): User ID.
        CreatedAt (datetime): Timestamp when the category was created.
        UpdatedAt (datetime): Timestamp when the category was last updated.
    """
    CategoryID = fields.Int(required=False, doc="Unique category ID")
    CategoryName = fields.Str(required=True, doc="Category name")
    CategoryType = fields.Str(required=True, doc="Category type (Expense or Income)")
    UserID = fields.Int(required=True, doc="User ID")
    CreatedAt = fields.DateTime(required=False, doc="Timestamp when the category was created")
    UpdatedAt = fields.DateTime(required=False, doc="Timestamp when the category was last updated")

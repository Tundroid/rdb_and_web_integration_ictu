#!/usr/bin/python
""" User class """


from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
import models
from marshmallow import Schema, fields
from datetime import datetime


class User(BaseModel, Base):
    """
    Representation of User.

    This class defines the User model, which stores user information.

    Attributes:
        UserID (int): Unique user ID.
        FullName (str): User's full name.
        Email (str): User's email address.
        UserPassword (str): User's password.
        CreatedAt (datetime): Timestamp when the user was created.
        UpdatedAt (datetime): Timestamp when the user was last updated.
    """
    if models.storage_t == "db":
        __tablename__ = 'User'
        __table_args__ = {'schema': 'fet_db'}

        UserID = Column(Integer, primary_key=True, autoincrement=True,
                    doc="Unique user ID")
        FullName = Column(String(100), nullable=False,
                          doc="User's full name")
        Email = Column(String(255), unique=True, nullable=False,
                      doc="User's email address")
        UserPassword = Column(String(255), nullable=False,
                              doc="User's password")
        CreatedAt = Column(TIMESTAMP, default=datetime.utcnow,
                           doc="Timestamp when the user was created")
        UpdatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,
                           doc="Timestamp when the user was last updated")


    def __init__(self, *args, **kwargs):
        """
        User initialization.

        Initializes the User object with the given arguments.
        """
        super().__init__(*args, **kwargs)


class UserSchema(Schema):
    """
    User schema.

    This schema defines the structure of the User data.

    Attributes:
        UserID (int): Unique user ID.
        FullName (str): User's full name.
        Email (str): User's email address.
        UserPassword (str): User's password.
        CreatedAt (datetime): Timestamp when the user was created.
        UpdatedAt (datetime): Timestamp when the user was last updated.
    """
    UserID = fields.Int(required=False, doc="Unique user ID")
    FullName = fields.Str(required=True, doc="User's full name")
    Email = fields.Email(required=True, doc="User's email address")
    UserPassword = fields.Str(required=True, doc="User's password")
    CreatedAt = fields.DateTime(required=False, doc="Timestamp when the user was created")
    UpdatedAt = fields.DateTime(required=False, doc="Timestamp when the user was last updated")

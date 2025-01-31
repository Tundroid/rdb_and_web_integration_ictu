#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.budget import Budget
from models.category import Category
from models.expense import Expense
from models.income import Income
from models.saving_goal import SavingGoal
from models.saving import Saving
from models.user import User
from os import getenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
    "budget": Budget,
    "category": Category,
    "expense": Expense,
    "income": Income,
    "saving_goal": SavingGoal,
    "saving": Saving,
    "user": User
}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        APP_MYSQL_USER = getenv("FET_MYSQL_USER")
        APP_MYSQL_PWD = getenv("FET_MYSQL_PWD")
        APP_MYSQL_HOST = getenv("FET_MYSQL_HOST")
        APP_MYSQL_DB = getenv("FET_MYSQL_DB")
        APP_ENV = getenv("FET_ENV")
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(
                    APP_MYSQL_USER,
                    APP_MYSQL_PWD,
                    APP_MYSQL_HOST,
                    APP_MYSQL_DB)
            )
        if APP_ENV == "test":
            pass

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        class_dict = classes
        if cls:
            class_dict = {key: val for key, val in class_dict.items() if val == cls}
        for my_class in class_dict.values():
            objs = self.__session.query(my_class).all()
            for obj in objs:
                obj_id = ("-".join([str(getattr(obj, k.name))
                                    for k in inspect(cls).primary_key]))
                key = f"{obj.__class__.__name__}.{obj_id}"
                new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        # TODO try to create all db with the following
        sess_factory = sessionmaker(bind=self.__engine,
                                    expire_on_commit=False)
        self.__session = scoped_session(sess_factory)

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, ids):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        return (self.__session.query(cls)
                        .filter_by(**ids).first())

    def count(self, cls=None):
        """
        count the number of objects in storage
        """

        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    def clean(self, cls):
        """
        clear all records in given table represented by @cls
        """
        # Disable foreign key checks
        self.__session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

        # Truncate the table
        self.__session.execute(text(f"TRUNCATE TABLE {cls.__tablename__}"))

        # Re-enable foreign key checks
        self.__session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        self.save()
    @property
    def session(self):
        """
        Getter for the private __session attribute.
        Provides controlled access to the database session.
        """
        return self.__session


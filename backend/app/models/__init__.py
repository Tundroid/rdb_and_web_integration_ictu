#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv

storage_t = getenv("APP_STORAGE_TYPE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    pass
storage.reload()

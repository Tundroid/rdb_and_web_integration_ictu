import unittest
from flask import Flask
from flask_jwt_extended import create_access_token
from api.v1.app import app 
from models import storage
from models.engine.db_storage import classes_commerce, classes_account
from unittest.mock import patch
import random
from sqlalchemy import inspect
from models.account_type import AccountType, AccountTypeSchema


class TestCreateAccountTypeEndpoint(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.token = create_access_token(identity="test_user")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def tearDown(self):
        """Clean up after each test."""
        self.app_context.pop()


    def test_create_account_type(self):
        """Test creating a new account type."""
        data = {"type_name": "New Account Type"}
        response = self.app.post("/api/v1/create/account_type", 
                                 headers=self.headers, json=data)
        self.assertEqual(response.status_code, 201)


    def test_create_account_type_invalid_data(self):
        """Test creating an account type with invalid data."""
        data = {"type_name": None}
        response = self.app.post("/api/v1/create/account_type", 
                                 headers=self.headers, json=data)
        self.assertEqual(response.status_code, 400)


    def test_create_account_type_duplicate(self):
        """Test creating a duplicate account type."""
        data = {"type_name": "Existing Account Type"}
        # Create an existing account type
        existing_account_type = AccountType(type_name=data["type_name"])
        storage.new(existing_account_type)
        storage.save()
        
        response = self.app.post("/api/v1/create/account_type", 
                                 headers=self.headers, json=data)
        self.assertEqual(response.status_code, 409)


    def test_create_account_type_empty_data(self):
        """Test creating an account type with empty data."""
        data = {}
        response = self.app.post("/api/v1/create/account_type", 
                                 headers=self.headers, json=data)
        self.assertEqual(response.status_code, 400)


    def test_create_account_type_invalid_json(self):
        """Test creating an account type with invalid JSON."""
        data = "Invalid JSON"
        response = self.app.post("/api/v1/create/account_type", 
                                 headers=self.headers, data=data)
        self.assertEqual(response.status_code, 400)


    def test_create_account_type_unauthorized(self):
        """Test creating an account type without authorization."""
        data = {"type_name": "New Account Type"}
        headers = {}
        response = self.app.post("/api/v1/create/account_type", 
                                 headers=headers, json=data)
        self.assertEqual(response.status_code, 401)


    def test_create_account_type_non_existent_model(self):
        """Test creating an account type for a non-existent model."""
        data = {"type_name": "New Account Type"}
        response = self.app.post("/api/v1/create/NonExistentModel", 
                                 headers=self.headers, json=data)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
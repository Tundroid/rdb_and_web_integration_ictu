import unittest
from flask import Flask
from flask_jwt_extended import create_access_token
from api.v1.app import app
from models import storage
from unittest.mock import patch
from models.engine.db_storage import classes_commerce, classes_account
import random
from sqlalchemy import inspect

class TestGetModelEndpoint(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.classes = classes_commerce | classes_account

        # Generate a JWT token for testing
        self.token = create_access_token(identity="test_user")

        # Set up test headers with the JWT token
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def tearDown(self):
        """Clean up after each test."""
        self.app_context.pop()


    def test_get_model_no_model(self):
        """Test when no model is provided."""
        # Simulate a GET request without providing a model
        response = self.app.get("/api/v1/get", headers=self.headers)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertIn("Model is required", response.json["message"])
        

    def test_get_all_models(self):
        """Test retrieving all instances of a model."""
        for model, model_cls in self.classes.items():
            # Simulate a GET request to the /get/model endpoint
            response = self.app.get(f"/api/v1/get/{model}", headers=self.headers)

            # Check the response
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), len(storage.all(model_cls)))

    def test_get_all_models_with_id(self):
        """Test retrieving all instances of a model with id."""
        for model, model_cls in self.classes.items():
            db_models = storage.all(model_cls)
            model_id = "NoID"
            if len(db_models):
                random_key = random.choice(list(db_models.keys()))
                m = db_models[random_key]
                model_id = ("-".join([str(getattr(m, k.name))
                                    for k in inspect(model_cls).primary_key]))    
            # Simulate a GET request to the /get/model endpoint
            response = self.app.get(f"/api/v1/get/{model}/{model_id}", headers=self.headers)

            # Check the response
            if len(db_models):
                self.assertEqual(response.status_code, 200)
                self.assertRegex(str(response.json), r'\{.+?\}')
            else:
                self.assertEqual(response.status_code, 404)
                self.assertRegex(response.json["message"], rf"Model `{model}` identified by `\[.*\]`")

    def test_get_non_model(self):
        """Test when getting non model."""
        model = "NonModel"
        # Simulate a GET request to the /get/model endpoint
        response = self.app.get(f"/api/v1/get/{model}", headers=self.headers)

        # Check the response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(f"Model `{model}`", response.json["message"])

    def test_get_non_model_and_id(self):
        """Test when getting non model with id."""
        id = "NoID"
        model = "NonModel"
        # Simulate a GET request to the /get/model endpoint
        response = self.app.get(f"/api/v1/get/{model}/{id}", headers=self.headers)

        # Check the response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(f"Model `{model}`", response.json["message"])

    # TODO test authorized requests

if __name__ == "__main__":
    unittest.main()

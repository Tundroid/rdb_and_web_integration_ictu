#!/usr/bin/python3
"""Create a flask application for the API"""

from os import getenv

from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views
import os
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

def create_app(config_name=None):
    """Application factory function to create a Flask app instance"""
    
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Register the blueprint(s)
    app.register_blueprint(app_views)
    
    # Configure JWT
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_default_secret_key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Token expiration time: 1 hour
    jwt = JWTManager(app)

    # Set up other app configurations if needed
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://user@localhost/dbname')

    @app.teardown_appcontext
    def close(exception):
        """Closes the storage"""
        storage.close()

    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors with a JSON response"""
        return jsonify({"error": "Not found"}), 404

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port="5120",
            threaded=True)

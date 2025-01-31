#!/usr/bin/python3
""" Model creator API endpoints """


# Standard library imports
import base64
import bcrypt

# Third-party imports
from flask import request, abort, jsonify
from flask_jwt_extended import jwt_required


# Local imports
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/login_user", methods=['POST'], strict_slashes=False)
# @jwt_required()
def login_user():
    """
    Create a new model instance.

    Args:
        model (str): The model name.
        request body: JSON data for the new model instance.

    Returns:
        JSON response with the created model data or an error message.

    Errors:
        400: Invalid request (e.g., missing model or invalid JSON)
        404: Model not found
        409: Resource already exists
    """

    # Get the Authorization header
    auth_header = request.headers.get('X-User-Credentials')

    if not auth_header:
        return abort(401, description={"message": "Authorization header is missing!"})


    # Ensure the header starts with 'Basic'
    if not auth_header.startswith('Basic '):
        abort(401, description={"message": "Invalid authentication type!"})

    # Extract the encoded credentials from the header
    encoded_credentials = auth_header.split(' ')[1]

    # Decode the base64-encoded credentials
    try:
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)  # Split into username and password
    except Exception as e:
        abort(400, description={"message": "Failed to decode credentials!"})

    # Here you can now use the `username` and `password` to validate the user
    # For example:C
    user = storage.session.query(User).filter_by(Email=username).first()

    if not user:
        abort(401, description={"message": "User not found!"})
    
    if not bcrypt.checkpw(password.encode('utf-8'), user.UserPassword.encode('utf-8')):
        abort(401, description={"message": "Password incorrect!"})
    
    return jsonify(user.to_dict())

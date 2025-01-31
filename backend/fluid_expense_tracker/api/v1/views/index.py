#!/usr/bin/python3
"""API main routes"""

from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes

from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required
)

# Test user for JWT
users = {
    "skfn": {"password": generate_password_hash("skfn")}
}

# Route to authenticate users and generate a JWT token
@app_views.route('/login', methods=['POST'])
def login():
    # Get Basic Auth credentials
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"msg": "Basic authentication required"}), 401

    # Validate user credentials
    user = users.get(auth.username)
    if not user or not check_password_hash(user['password'], auth.password):
        return jsonify({"msg": "Invalid username or password"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=auth.username)
    return jsonify(access_token=access_token), 200


@app_views.route("/status", strict_slashes=False)
@jwt_required()
def status():
    """Returns the status in JSON format"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
@jwt_required()
def stats():
    """Endpoint that retrieves the number of each objects by type"""
    stats_dict = {}
    for cls_name, cls in classes.items():
        stats_dict[cls_name] = storage.count(cls)
    return jsonify(stats_dict)

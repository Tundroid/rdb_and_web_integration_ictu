#!/usr/bin/python3
""" Model getter API endpoints """

from flask import abort, jsonify, request
from models.category import Category
from models import storage
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import BadRequest
from marshmallow import Schema, fields, validates, ValidationError


@app_views.route("/delete_category", methods=['DELETE'], strict_slashes=False)
# @jwt_required()
def delete_category():
    """Retrieve model or model instance details.

    Args:
        model (str): The model name.
        user_id (str): The ID of the model instance (optional).

    Returns:
        JSON response with model data or an error message.
    """
    
    try:
        filters = request.args
        CategoryFilterSchema().load(filters)
        
        query = storage.session.query(Category).filter(Category.UserID.in_([1, filters["UserID"]]))
        query = query.filter(Category.CategoryID == filters["CategoryID"])

        category = query.first()
        if category:
            storage.delete(category)
            storage.save()
        return '', 200
    except ValidationError as e:
        abort(400, description={"message":  e.messages})


class CategoryFilterSchema(Schema):
    UserID = fields.Integer(required=True)
    CategoryID = fields.Integer(required=True)



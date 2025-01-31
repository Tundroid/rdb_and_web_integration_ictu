#!/usr/bin/python3
""" Model getter API endpoints """

from flask import abort, jsonify, request
from models.category import Category
from models import storage
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import BadRequest
from marshmallow import Schema, fields, validates, ValidationError


@app_views.route("/get_list_category", methods=['GET'], strict_slashes=False)
# @jwt_required()
def get_categories():
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
        
        query = storage.session.query(
                Category.CategoryID,
                Category.CategoryName,
                Category.CategoryType
            )

        if "UserID" in filters:
            query = query.filter(Category.UserID.in_([1, filters["UserID"]]))


        results = query.all()

        schema = CategoryCategorySchema(many=True)
        serialized_data = schema.dump(results)
        return jsonify(serialized_data)
    except ValidationError as e:
        abort(400, description={"message":  e.messages})


class CategoryCategorySchema(Schema):
    CategoryID = fields.Integer()
    CategoryName = fields.String()
    CategoryType = fields.String()


class CategoryFilterSchema(Schema):
    UserID = fields.Integer(required=False)

    @validates('UserID')
    def validate_user_id(self, value):
        if value and value < 0:
            raise ValidationError('UserID must be a positive integer')


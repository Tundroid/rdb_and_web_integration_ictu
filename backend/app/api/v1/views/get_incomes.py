#!/usr/bin/python3
""" Model getter API endpoints """

from flask import abort, jsonify, request
from models.income import Income
from models.category import Category
from models import storage
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import BadRequest
from marshmallow import Schema, fields, validates, ValidationError


@app_views.route("/get_list_income", methods=['GET'], strict_slashes=False)
# @jwt_required()
def get_incomes():
    """Retrieve model or model instance details.

    Args:
        model (str): The model name.
        user_id (str): The ID of the model instance (optional).

    Returns:
        JSON response with model data or an error message.
    """
    
    try:
        filters = request.args
        IncomeFilterSchema().load(filters)
        
        query = storage.session.query(
                Income.IncomeID,
                Income.Amount,
                Income.IncomeDate,
                Income.IncomeTime,
                # Income.Recurring,
                Income.IncomeDescription,
                Category.CategoryName
            ).join(Category, Income.CategoryID == Category.CategoryID)

        if "UserID" in filters:
            query = query.filter(Income.UserID == filters["UserID"])

        results = query.all()

        schema = IncomeCategorySchema(many=True)
        serialized_data = schema.dump(results)
        return jsonify(serialized_data)
    except ValidationError as e:
        abort(400, description={"message":  e.messages})


class IncomeCategorySchema(Schema):
    IncomeID = fields.Integer()
    Amount = fields.Integer()
    IncomeDate = fields.Date()
    IncomeTime = fields.Time()
    # Recurring = fields.Boolean()
    IncomeDescription = fields.String()
    CategoryName = fields.String()


class IncomeFilterSchema(Schema):
    UserID = fields.Integer(required=False)

    @validates('UserID')
    def validate_user_id(self, value):
        if value and value < 0:
            raise ValidationError('UserID must be a positive integer')


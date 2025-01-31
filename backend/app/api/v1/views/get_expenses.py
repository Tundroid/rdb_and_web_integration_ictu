#!/usr/bin/python3
""" Model getter API endpoints """

from flask import abort, jsonify, request
from ictu.rdb_and_web_integration.backend.app.models.program import Expense
from ictu.rdb_and_web_integration.backend.app.models.department import Category
from models import storage
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import BadRequest
from marshmallow import Schema, fields, validates, ValidationError


@app_views.route("/get_list_expense", methods=['GET'], strict_slashes=False)
# @jwt_required()
def get_expenses():
    """Retrieve model or model instance details.

    Args:
        model (str): The model name.
        user_id (str): The ID of the model instance (optional).

    Returns:
        JSON response with model data or an error message.
    """
    
    try:
        filters = request.args
        ExpenseFilterSchema().load(filters)
        
        query = storage.session.query(
                Expense.ExpenseID,
                Expense.Amount,
                Expense.ExpenseDate,
                Expense.ExpenseTime,
                Expense.Recurring,
                Expense.ExpenseDescription,
                Category.CategoryName
            ).join(Category, Expense.CategoryID == Category.CategoryID)

        if "UserID" in filters:
            query = query.filter(Expense.UserID == filters["UserID"])

        results = query.all()

        schema = ExpenseCategorySchema(many=True)
        serialized_data = schema.dump(results)
        return jsonify(serialized_data)
    except ValidationError as e:
        abort(400, description={"message":  e.messages})


class ExpenseCategorySchema(Schema):
    ExpenseID = fields.Integer()
    Amount = fields.Integer()
    ExpenseDate = fields.Date()
    ExpenseTime = fields.Time()
    Recurring = fields.Boolean()
    ExpenseDescription = fields.String()
    CategoryName = fields.String()


class ExpenseFilterSchema(Schema):
    UserID = fields.Integer(required=False)

    @validates('UserID')
    def validate_user_id(self, value):
        if value and value < 0:
            raise ValidationError('UserID must be a positive integer')


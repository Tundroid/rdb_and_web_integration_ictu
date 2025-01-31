#!/usr/bin/python3
""" Model creator API endpoints """

from flask import request, jsonify, abort
from models.engine.db_storage import classes
from models import storage
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect
from marshmallow import Schema, fields, validates, ValidationError

@app_views.route("/delete", methods=['DELETE'], strict_slashes=False)
@app_views.route("/delete/<model>", methods=['DELETE'], strict_slashes=False)
# @jwt_required()
def delete_model(model=None):
    """Delete a new model instance.

    Args:
        model (str): The model name.
        request body: JSON data for the new model instance.

    Returns:
        JSON response with the created model data or an error message.
    """
    if (not model):
        abort(400, description={"message": "Model is required"})

    try:
        # data = request.get_json(silent=True)
        # print("data:", request.data)
        # print("headers:", request.headers)
        # if not data:
        #     print("No data")
        #     abort(400, description="Valid JSON data required")

        model_cls = classes[model]
        filters = request.args
        filters = eval(f"{model_cls.__name__}FilterSchema")().load(filters)
        print("Type: ", type(filters))
        print("Value: ", filters)

        category = storage.get(model_cls, filters)
        if category:
            storage.delete(category)
            storage.save()
        return '', 200
    except (KeyError, ValueError) as e:
        abort(404, description={"message": f"Model `{model}`"})
    except (IntegrityError) as e:
        abort(409, description={"message": f"Resource already exists in Model `{model}`"})
    except ValidationError as e:
        abort(400, description={"message":  e.messages})


class CategoryFilterSchema(Schema):
    UserID = fields.Integer(required=True)
    CategoryID = fields.Integer(required=True)

class ExpenseFilterSchema(Schema):
    UserID = fields.Integer(required=True)
    ExpenseID = fields.Integer(required=True)
    
class IncomeFilterSchema(Schema):
    UserID = fields.Integer(required=True)
    IncomeID = fields.Integer(required=True)
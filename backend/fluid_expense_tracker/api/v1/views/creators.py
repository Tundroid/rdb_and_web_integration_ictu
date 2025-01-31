#!/usr/bin/python3
""" Model creator API endpoints """


# Standard library imports
import importlib
import re
import bcrypt


# Third-party imports
from flask import request, abort
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest


# Local imports
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route("/create", methods=['POST'], strict_slashes=False)
@app_views.route("/create/<model>", methods=['POST'], strict_slashes=False)
# @jwt_required()
def create_model(model=None):
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
    if not model:
        abort(400, description={"message": "Model is required"})

    try:
        request_data = request.get_json(silent=True)
        if not request_data:
            raise BadRequest()

        db_model = classes[model]
        
        schema_module = importlib.import_module(f"models.{model}")
        schema_cls = getattr(schema_module, f"{db_model.__name__}Schema")
        schema = schema_cls(many=True) if type(request_data) is list else schema_cls()

        # Validate the data
        request_data = schema.load(request_data)

        data_set = [request_data] if type(request_data) is dict else request_data
        for data in data_set:
            if model == "user":
                data["UserPassword"] = bcrypt.hashpw(data["UserPassword"].encode('utf-8'), bcrypt.gensalt())
            obj = db_model(**data)
            storage.new(obj)
        storage.save()
        return {}, 201
    except KeyError:
        abort(404, description={"message": f"Model `{model}`"})
    except IntegrityError as e:
        match = re.search(r"Duplicate entry '(.+?)'", str(e.orig))
        duplicate_value = match.group(1) if match else "Unknown"
        abort(409, description={"message": f"Resource(s) already exists in Model `{model}`, check value(s) `{duplicate_value}`"})
    except ValidationError as e:
        msg = {"message": f"Error(s) found in data for Model `{model}`, see details"}
        msg["detail"] = e.messages
        abort(400, description=msg)
    except BadRequest:
        abort(400, description={"message": "Valid JSON data required"})

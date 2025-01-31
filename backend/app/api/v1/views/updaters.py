#!/usr/bin/python3
""" Model creator API endpoints """


import re

from flask import request, jsonify, abort
from models.engine.db_storage import classes
from models import storage
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect

@app_views.route("/update", methods=['PUT'], strict_slashes=False)
@app_views.route("/update/<model>", methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_model(model=None):
    """Update a new model instance.

    Args:
        model (str): The model name.
        request body: JSON data for the new model instance.

    Returns:
        JSON response with the created model data or an error message.
    """
    if (not model):
        abort(400, description="Model is required")

    try:
        data = request.get_json(silent=True)
        if not data:
            abort(400, description="Valid JSON data required")

        data = [data] if type(data) is dict else data
        for piece in data:
            db_model = storage.get(classes[model], piece[inspect(classes[model]).primary_key[0].name])
            for key, value in piece.items():
                # if key not in ignore:
                setattr(db_model, key, value)
        storage.save()
        
        return jsonify(db_model.to_dict()), 200
    except (KeyError, ValueError) as e:
        abort(404, description={"message":  f"Model `{model}`"})
    except (IntegrityError) as e:
        match = re.search(r"Duplicate entry '(.+?)'", str(e.orig))
        duplicate_value = match.group(1) if match else "Unknown"
        abort(409, description={"message": f"Resource(s) already exists in Model `{model}`, check value(s) `{duplicate_value}`"})

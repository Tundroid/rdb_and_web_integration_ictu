#!/usr/bin/python3
""" Model getter API endpoints """

from flask import abort, jsonify, request
from models.engine.db_storage import classes
from models import storage
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import OperationalError


@app_views.route("/util/clean", methods=['POST'], strict_slashes=False)
@jwt_required()
def clean_model():
    """Retrieve model or model instance details.

    Args:
        model (str): The model name.
        model_id (str): The ID of the model instance (optional).

    Returns:
        JSON response with model data or an error message.
    """
    if request.path == '/api/v1/util':
        abort(404, description={"message":  "Action is required"})

    request_data = None
    try:
        request_data = request.get_json(silent=True)
        if not request_data:
            raise BadRequest()
    except BadRequest:
                    abort(400, description={"message":  f"Valid JSON data required"})
    
    try:
        if "models" not in request_data.keys():
            abort(400, description={"message":  f"field `models` missing in JSON data"})
        
        models = request_data['models']
        for model in models:            
            storage.clean(classes[model])
        return '', 200
    except TypeError:
            abort(400, description={"message":  f"field `models` is not a valid list in JSON data"})
    except KeyError:
        abort(404, description={"message":  f"Model `{model}`"})
    except OperationalError as e:
        abort(500, description={"message":  f"MySQL error", "detail": str(e.orig)})

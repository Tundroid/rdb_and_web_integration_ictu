#!/usr/bin/python3
""" Model getter API endpoints """

from flask import abort, jsonify, request
from models.engine.db_storage import classes
from models import storage
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from werkzeug.exceptions import BadRequest



@app_views.route("/get", methods=['GET'], strict_slashes=False)
@app_views.route("/get/<model>", methods=['GET'], strict_slashes=False)
@app_views.route("/get/<model>/<model_id>", methods=['GET'], strict_slashes=False)
# @jwt_required()
def get_model(model=None, model_id=None):
    """Retrieve model or model instance details.

    Args:
        model (str): The model name.
        model_id (str): The ID of the model instance (optional).

    Returns:
        JSON response with model data or an error message.
    """
    if (not model):
        abort(400, description={"message":  "Model is required"})
    
    try:
        model_cls = classes[model]
        model_ids = None
        if request.data:
            try:
                data = request.get_json()
                ids = data['ids']
                keys = inspect(model_cls).primary_key
                model_ids = {key.name: ids[i] for i, key in enumerate(keys)}
            except KeyError:
                if not model_id:
                    abort(400, description={"message":  f"`ids` missing in JSON data"})
            except IndexError:
                if not model_id:
                    abort(400, description={"message":  f"`ids` length is short in JSON data"})
            except TypeError:
                if not model_id:
                    abort(400, description={"message":  f"Invalid JSON data or `ids` is not a valid list in JSON data"})
            except BadRequest:
                if not model_id:
                    abort(400, description={"message":  f"Valid JSON data required"})
        if not model_ids and model_id:
            model_ids = {inspect(model_cls).primary_key[0].name: model_id}

        if model_ids:
            db_model = storage.get(model_cls, model_ids)
            if db_model:
                return jsonify(db_model.to_dict())
            model_ids = [id for id in model_ids.values()]
            abort(404, description={"message":  f"Model `{model}` identified by `{model_ids}`"})

        """get all model details"""
        db_models = [obj.to_dict() for obj in storage.all(model_cls).values()]
        return jsonify(db_models)
    except (KeyError):
        abort(404, description={"message":  f"Model `{model}`"})

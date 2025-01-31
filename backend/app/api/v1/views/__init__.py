#!/usr/bin/python3
"""Create a flask application for the API"""

from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

@app_views.errorhandler(400)
def handle_bad_request(error):
    return handler_helper(error), 400

@app_views.errorhandler(401)
def handle_bad_request(error):
    return handler_helper(error), 401

@app_views.errorhandler(404)
def handle_not_found(error):
    return handler_helper(error), 404

@app_views.errorhandler(409)
def handle_conflict(error):
    return handler_helper(error), 409

def handler_helper(error):
    ret = {}
    ret["type"] = "error"
    ret["message"] = error.description["message"]
    if "detail" in error.description.keys():
        ret["detail"] = error.description["detail"]
    return jsonify(ret)


from api.v1.views.index import *
from api.v1.views.creators import *
from api.v1.views.readers import *
from api.v1.views.updaters import *
from api.v1.views.deleters import *
from api.v1.views.utils import *
from api.v1.views.get_expenses import *
from api.v1.views.get_incomes import *
from api.v1.views.get_categories import *
from api.v1.views.login_user import *

#!/usr/bin/python3
""" Model getter API endpoints """

from flask import abort, jsonify, request
from models.program import Program
from models.department import Department
from models import storage
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import BadRequest
from marshmallow import Schema, fields, validates, ValidationError


@app_views.route("/get_list_program", methods=['GET'], strict_slashes=False)
# @jwt_required()
def get_programs():
    """Retrieve model or model instance details.

    Args:
        model (str): The model name.
        user_id (str): The ID of the model instance (optional).

    Returns:
        JSON response with model data or an error message.
    """
    
    try:
        # filters = request.args
        # ProgramFilterSchema().load(filters)
        
        query = storage.session.query(
                Program.ProgramCode,
                Program.ProgramName,
                Department.DepartmentName,
                Program.Duration
            ).join(Department, Program.DepartmentID == Department.DepartmentID)

        # if "UserID" in filters:
        #     query = query.filter(Program.UserID == filters["UserID"])

        results = query.all()

        schema = ProgramsSchema(many=True)
        serialized_data = schema.dump(results)
        return jsonify(serialized_data)
    except ValidationError as e:
        abort(400, description={"message":  e.messages})


class ProgramsSchema(Schema):
    ProgramCode = fields.String()
    ProgramName = fields.String()
    DepartmentName = fields.String()
    Duration = fields.Int()


class ProgramFilterSchema(Schema):
    UserID = fields.Integer(required=False)

    @validates('UserID')
    def validate_user_id(self, value):
        if value and value < 0:
            raise ValidationError('UserID must be a positive integer')


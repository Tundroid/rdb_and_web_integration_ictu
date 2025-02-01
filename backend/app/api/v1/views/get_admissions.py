#!/usr/bin/python3
""" Model getter API endpoints """

from flask import abort, jsonify, request
from models.admission import Admission
from models.applicant import Applicant
from models.program import Program
from models.department import Department
from models import storage
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import BadRequest
from marshmallow import Schema, fields, validates, ValidationError


@app_views.route("/get_list_admission", methods=['GET'], strict_slashes=False)
# @jwt_required()
def get_admissions():
    """Retrieve model or model instance details.

    Args:
        model (str): The model name.
        user_id (str): The ID of the model instance (optional).

    Returns:
        JSON response with model data or an error message.
    """
    
    try:
        # filters = request.args
        # AdmissionFilterSchema().load(filters)
        
        query = storage.session.query(
                Admission.AdmissionID,
                Applicant.FullName,
                Program.ProgramName,
                Department.DepartmentName,
                Admission.ApplicationDate,
                Admission.ApplicationStatus
            ).join(Applicant, Admission.ApplicantID == Applicant.ApplicantID)\
                .join(Program, Admission.ProgramCode == Program.ProgramCode)\
                    .join(Department, Program.DepartmentID == Department.DepartmentID)

        # if "UserID" in filters:
        #     query = query.filter(Admission.UserID == filters["UserID"])

        results = query.all()

        schema = AdmissionsSchema(many=True)
        serialized_data = schema.dump(results)
        return jsonify(serialized_data)
    except ValidationError as e:
        abort(400, description={"message":  e.messages})


class AdmissionsSchema(Schema):
    AdmissionID = fields.Int()
    FullName = fields.String()
    ProgramName = fields.String()
    DepartmentName = fields.String()
    ApplicationDate = fields.Date()
    ApplicationStatus = fields.String()


class AdmissionFilterSchema(Schema):
    UserID = fields.Integer(required=False)

    @validates('UserID')
    def validate_user_id(self, value):
        if value and value < 0:
            raise ValidationError('UserID must be a positive integer')


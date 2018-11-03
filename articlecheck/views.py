from flask import request, jsonify, abort
from jsonschema import validate, ValidationError
from app import app
from conditions import Group, CalculationError
from schemas import CONDITIONS_SCHEMA


@app.route("/api/v1/conditions/", methods=["POST"])
def conditions():
    input_data = request.get_json()
    if input_data:
        try:
            validate(input_data, CONDITIONS_SCHEMA)
            conditions = Group(input_data["article"], **input_data["conditions"])
            verbose_result = conditions.get_verbose_result()
            return jsonify(verbose_result)
        except (ValidationError, CalculationError) as e:
            return abort(400, {"errors": e.message})
    else:
        return abort(400, {'errors': 'Invalid JSON'})

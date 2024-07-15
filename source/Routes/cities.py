from flask import Blueprint, request, jsonify, abort
from src.controllers.cities import (
    create_city,
    delete_city,
    get_city_by_id,
    get_cities,
    update_city,
)
from marshmallow import Schema, fields, ValidationError
from flask_httpauth import HTTPBasicAuth

# Define a schema for city data validation using Marshmallow
class CitySchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(missing=None)

city_schema = CitySchema()

# Initialize Blueprint and basic authentication
cities_bp = Blueprint("cities", __name__, url_prefix="/cities")
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Replace with your method to verify user credentials
    return username == "admin" and password == "secret"

# Route to retrieve all cities
@cities_bp.route("/", methods=["GET"])
def get_all_cities():
    cities = get_cities()
    return jsonify([city_schema.dump(city) for city in cities])

# Route to create a new city
@cities_bp.route("/", methods=["POST"])
@auth.login_required
def post_city():
    try:
        data = city_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    city = create_city(data)
    return jsonify(city_schema.dump(city)), 201

# Route to retrieve a specific city by ID
@cities_bp.route("/<int:city_id>", methods=["GET"])
def show_city(city_id):
    city = get_city_by_id(city_id)
    if not city:
        abort(404, description="City not found")
    return jsonify(city_schema.dump(city))

# Route to update a specific city
@cities_bp.route("/<int:city_id>", methods=["PUT"])
@auth.login_required
def put_city(city_id):
    city = get_city_by_id(city_id)
    if not city:
        abort(404, description="City not found")
    try:
        data = city_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    updated_city = update_city(city_id, data)
    return jsonify(city_schema.dump(updated_city))

# Route to delete a specific city
@cities_bp.route("/<int:city_id>", methods=["DELETE"])
@auth.login_required
def delete_specific_city(city_id):
    if delete_city(city_id):
        return '', 204
    else:
        abort(404, description="City not found")

# Authentication error handler
@auth.error_handler
def auth_error():
    return jsonify({"error": "Authentication required"}), 401


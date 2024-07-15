from flask import Blueprint, jsonify, abort
from src.controllers.countries import (
    get_countries,
    get_country_by_code,
    get_country_cities,
)
from marshmallow import Schema, fields, ValidationError
from flask_httpauth import HTTPBasicAuth

# Initialize the blueprint and authentication handler
countries_bp = Blueprint("countries", __name__, url_prefix="/countries")
auth = HTTPBasicAuth()

# Define a schema for country code validation using Marshmallow
class CountryCodeSchema(Schema):
    code = fields.String(required=True, validate=lambda x: len(x) == 2 and x.isalpha())

country_code_schema = CountryCodeSchema()

@auth.verify_password
def verify_password(username, password):
    # Implement your verification logic here
    return username == "admin" and password == "securepassword"

# Error handler for 404 Not Found
@countries_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

# Route to retrieve all countries
@countries_bp.route("/", methods=["GET"])
def get_all_countries():
    countries = get_countries()
    return jsonify([country for country in countries]), 200

# Route to retrieve a specific country by code
@countries_bp.route("/<code>", methods=["GET"])
def show_country(code):
    errors = country_code_schema.validate({'code': code})
    if errors:
        abort(400, description=f"Validation error: {errors}")
    country = get_country_by_code(code)
    if country is None:
        abort(404, description="Country not found")
    return jsonify(country), 200

# Route to retrieve cities of a specific country
@countries_bp.route("/<code>/cities", methods=["GET"])
def show_country_cities(code):
    errors = country_code_schema.validate({'code': code})
    if errors:
        abort(400, description=f"Validation error: {errors}")
    cities = get_country_cities(code)
    if cities is None:
        abort(404, description="Cities not found for the given country code")
    return jsonify(cities), 200

# Optional: Secure POST, PUT, DELETE routes with authentication
@countries_bp.route("/secure", methods=["POST", "PUT", "DELETE"])
@auth.login_required
def modify_countries():
    if request.method == "POST":
        # Implementation for creating a country
        pass
    elif request.method == "PUT":
        # Implementation for updating a country
        pass
    elif request.method == "DELETE":
        # Implementation for deleting a country
        pass
    return jsonify(message="Operation successful"), 200


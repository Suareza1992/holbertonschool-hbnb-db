from flask import Blueprint, request, jsonify, abort
from src.controllers.amenities import (
    create_amenity,
    delete_amenity,
    get_amenity_by_id,
    get_amenities,
    update_amenity,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Blueprint
amenities_bp = Blueprint("amenities", __name__, url_prefix="/amenities")

# Setup rate limiting
limiter = Limiter(key_func=get_remote_address)

# Decorator for handling common HTTP errors
def handle_errors(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except KeyError as e:
            abort(400, description=f"Missing data: {str(e)}")
        except ValueError as e:
            abort(422, description=str(e))
    wrapper.__name__ = f.__name__
    return wrapper

@amenities_bp.route("/", methods=["GET"])
@limiter.limit("100 per minute")
def get_all_amenities():
    """Retrieve all amenities."""
    return get_amenities()

@amenities_bp.route("/", methods=["POST"])
@limiter.limit("50 per hour")
@handle_errors
def post_amenity():
    """Create a new amenity."""
    if not request.json:
        abort(400, description="Invalid data provided.")
    return create_amenity(request.json)

@amenities_bp.route("/<string:amenity_id>", methods=["GET"])
def show_amenity(amenity_id):
    """Retrieve a specific amenity by ID."""
    return get_amenity_by_id(amenity_id)

@amenities_bp.route("/<string:amenity_id>", methods=["PUT"])
@handle_errors
def put_amenity(amenity_id):
    """Update a specific amenity."""
    data = request.get_json()
    if not data:
        abort(400, description="Invalid data provided.")
    return update_amenity(amenity_id, data)

@amenities_bp.route("/<string:amenity_id>", methods=["DELETE"])
def delete_specific_amenity(amenity_id):
    """Delete a specific amenity."""
    return delete_amenity(amenity_id)


from flask import Blueprint, request, jsonify, abort
from src.controllers.places import (
    create_place,
    delete_place,
    get_place_by_id,
    get_places,
    update_place,
)
from src.schemas.place_schema import PlaceSchema  # Ensure this schema is properly defined
from marshmallow import ValidationError
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the blueprint
places_bp = Blueprint("places", __name__, url_prefix="/places")
place_schema = PlaceSchema()

# Route to get all places
@places_bp.route("/", methods=["GET"])
def get_all_places():
    places = get_places()
    return jsonify([place_schema.dump(place) for place in places]), 200

# Route to create a new place
@places_bp.route("/", methods=["POST"])
def post_place():
    json_data = request.get_json()
    if not json_data:
        logger.error("No input data provided")
        abort(400, description="No input data provided")
    try:
        data = place_schema.load(json_data)
        place = create_place(data)
        return jsonify(place_schema.dump(place)), 201
    except ValidationError as err:
        logger.warning(f"Validation errors: {err.messages}")
        abort(400, description=f"Validation errors: {err.messages}")

# Route to get a specific place by ID
@places_bp.route("/<int:place_id>", methods=["GET"])
def show_place(place_id):
    try:
        place = get_place_by_id(place_id)
        if not place:
            logger.info(f"Place with id {place_id} not found")
            abort(404, description=f"Place with id {place_id} not found")
        return jsonify(place_schema.dump(place)), 200
    except Exception as e:
        logger.error(f"Error getting place with id {place_id}: {e}")
        abort(500, description="Internal Server Error")

# Route to update a specific place
@places_bp.route("/<int:place_id>", methods=["PUT"])
def put_place(place_id):
    place = get_place_by_id(place_id)
    if not place:
        abort(404, description=f"Place with id {place_id} not found")
    json_data = request.get_json()
    if not json_data:
        abort(400, description="No input data provided")
    try:
        data = place_schema.load(json_data)
        updated_place = update_place(place_id, data)
        return jsonify(place_schema.dump(updated_place)), 200
    except ValidationError as err:
        abort(400, description=f"Validation errors: {err.messages}")

# Route to delete a specific place
@places_bp.route("/<int:place_id>", methods=["DELETE"])
def delete_specific_place(place_id):
    if delete_place(place_id):
        logger.info(f"Deleted place with id {place_id}")
        return '', 204
    else:
        logger.warning(f"Failed to delete place with id {place_id}")
        abort(404, description=f"Place with id {place_id} not found")


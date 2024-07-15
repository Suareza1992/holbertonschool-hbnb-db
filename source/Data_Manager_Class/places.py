"""
Places controller module
"""

from flask import request, jsonify, abort, Blueprint
from src.models.place import Place
from flask_jwt_extended import jwt_required
from src.controllers.login import check_admin
import logging
from marshmallow import Schema, fields, validate, ValidationError

# Initialize logging
logger = logging.getLogger(__name__)

# Blueprint for places
bp = Blueprint('places', __name__)

class PlaceSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(required=True)

place_schema = PlaceSchema()

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        if not check_admin():
            logger.warning("Unauthorized access attempt.")
            return jsonify({'msg': 'Not allowed'}), 403
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/places', methods=['GET'])
def get_places():
    """Returns all places"""
    places = Place.get_all()
    return jsonify([place.to_dict() for place in places]), 200

@bp.route('/places', methods=['POST'])
@admin_required
def create_place():
    """Creates a new place"""
    try:
        data = place_schema.load(request.get_json())
        place = Place.create(data)
        logger.info(f'Place created with ID {place.id}')
        return jsonify(place.to_dict()), 201
    except ValidationError as err:
        return jsonify(err.messages), 422

@bp.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    """Returns a place by ID"""
    place = Place.get(place_id)
    if not place:
        logger.info(f"Place with ID {place_id} not found")
        abort(404, f"Place with ID {place_id} not found")
    return jsonify(place.to_dict()), 200

@bp.route('/places/<place_id>', methods=['PUT'])
@admin_required
def update_place(place_id):
    """Updates a place by ID"""
    try:
        data = place_schema.load(request.get_json())
        place = Place.update(place_id, data)
        if not place:
            logger.info(f"Failed to update place with ID {place_id}")
            abort(404, f"Place with ID {place_id} not found")
        logger.info(f"Place with ID {place_id} updated successfully")
        return jsonify(place.to_dict()), 200
    except ValidationError as err:
        return jsonify(err.messages), 422

@bp.route('/places/<place_id>', methods=['DELETE'])
@admin_required
def delete_place(place_id):
    """Deletes a place by ID"""
    if Place.delete(place_id):
        logger.info(f"Place with ID {place_id} deleted successfully")
        return '', 204
    logger.info(f"Failed to delete place with ID {place_id}")
    abort(404, f"Place with ID {place_id} not found")


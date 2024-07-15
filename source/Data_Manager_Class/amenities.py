"""
Amenity controller module
"""

from flask import abort, request, jsonify
from flask_jwt_extended import jwt_required
from src.controllers.login import check_admin
from src.models.amenity import Amenity
import logging

# Setup logging
logger = logging.getLogger(__name__)

@jwt_required()  # Ensure all routes are protected with JWT
def get_amenities():
    """Returns all amenities."""
    amenities = Amenity.get_all()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200

@jwt_required()
def create_amenity():
    """Creates a new amenity. Only accessible by admins."""
    if not check_admin():
        logger.warning("Unauthorized attempt to create amenity")
        return jsonify({"msg": "Administration rights required"}), 403
    
    data = request.get_json()
    try:
        amenity = Amenity.create(data)
        return jsonify(amenity.to_dict()), 201
    except KeyError as e:
        logger.error(f"Missing field {e} in data", exc_info=True)
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        logger.error(f"Invalid value in data: {e}", exc_info=True)
        abort(400, str(e))

@jwt_required()
def get_amenity_by_id(amenity_id: str):
    """Returns a specific amenity by ID."""
    amenity = Amenity.get(amenity_id)
    if not amenity:
        logger.info(f"Amenity with ID {amenity_id} not found")
        abort(404, f"Amenity with ID {amenity_id} not found")
    return jsonify(amenity.to_dict()), 200

@jwt_required()
def update_amenity(amenity_id: str):
    """Updates a specific amenity by ID. Only accessible by admins."""
    if not check_admin():
        logger.warning("Unauthorized attempt to update amenity")
        return jsonify({"msg": "Administration rights required"}), 403
    
    data = request.get_json()
    updated_amenity = Amenity.update(amenity_id, data)
    if not updated_amenity:
        logger.info(f"Amenity with ID {amenity_id} not found for update")
        abort(404, f"Amenity with ID {amenity_id} not found")
    return jsonify(updated_amenity.to_dict()), 200

@jwt_required()
def delete_amenity(amenity_id: str):
    """Deletes a specific amenity by ID. Only accessible by admins."""
    if not check_admin():
        logger.warning("Unauthorized attempt to delete amenity")
        return jsonify({'msg': 'Not allowed'}), 403

    if not Amenity.delete(amenity_id):
        logger.info(f"Amenity with ID {amenity_id} not found for deletion")
        abort(404, f"Amenity with ID {amenity_id} not found")
    logger.info(f"Amenity {amenity_id} deleted successfully")
    return "", 204


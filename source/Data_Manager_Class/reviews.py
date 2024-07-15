"""
Reviews controller module
"""

from flask import Blueprint, request, jsonify, abort
from src.models.review import Review
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
import logging

# Setup Blueprint and logging
bp = Blueprint('reviews', __name__)
logger = logging.getLogger(__name__)

class ReviewSchema(Schema):
    user_id = fields.Int(required=True)
    content = fields.Str(required=True)

review_schema = ReviewSchema()

@app.errorhandler(400)
def handle_400_error(e):
    return jsonify(error='Bad Request', message=str(e)), 400

@app.errorhandler(404)
def handle_404_error(e):
    return jsonify(error='Not Found', message=str(e)), 404

@app.errorhandler(422)
def handle_422_error(e):
    return jsonify(error='Unprocessable Entity', message=str(e)), 422

@app.errorhandler(403)
def handle_403_error(e):
    return jsonify(error='Forbidden', message=str(e)), 403

@bp.route('/reviews', methods=['GET'])
def get_reviews():
    """Returns all reviews"""
    reviews = Review.get_all()
    return jsonify([review.to_dict() for review in reviews]), 200

@bp.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    """Creates a new review"""
    user_id = get_jwt_identity()
    json_data = request.get_json()
    try:
        data = review_schema.load(json_data)
        data['user_id'] = user_id
        review = Review.create(data)
        return jsonify(review.to_dict()), 201
    except ValidationError as err:
        abort(422, str(err.messages))

@bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review_by_id(review_id):
    """Returns a review by ID"""
    review = Review.get(review_id)
    if not review:
        abort(404, f'Review with ID {review_id} not found')
    return jsonify(review.to_dict()), 200

@bp.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """Updates a review by ID"""
    user_id = get_jwt_identity()
    if not is_review_owner_or_admin(review_id, user_id):
        abort(403, 'Not allowed')
    
    json_data = request.get_json()
    try:
        data = review_schema.load(json_data)
        review = Review.update(review_id, data)
        if not review:
            abort(404, f'Review with ID {review_id} not found')
        return jsonify(review.to_dict()), 200
    except ValidationError as err:
        abort(422, str(err.messages))

@bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Deletes a review by ID"""
    user_id = get_jwt_identity()
    if not is_review_owner_or_admin(review_id, user_id):
        abort(403, 'Not allowed')
    
    if Review.delete(review_id):
        logger.info(f'Review {review_id} deleted by user {user_id}')
        return '', 204
    else:
        abort(404, f'Review with ID {review_id} not found')

def is_review_owner_or_admin(review_id, user_id):
    review = Review.get(review_id)
    if review and (review.user_id == user_id or check_admin()):
        return True
    return False


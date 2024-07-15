from flask import Blueprint, request, jsonify, abort
from src.controllers.reviews import (
    create_review,
    delete_review,
    get_review_by_id,
    get_reviews,
    update_review,
    get_reviews_from_place,
    get_reviews_from_user,
)
from src.schemas.review_schema import ReviewSchema  # Ensure this schema is properly defined
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the blueprint
reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")
review_schema = ReviewSchema()

# Define routes
@reviews_bp.route("/places/<int:place_id>/reviews", methods=["POST"])
@jwt_required()
def create_place_review(place_id):
    try:
        user_id = get_jwt_identity()
        data = review_schema.load(request.get_json())
        review = create_review(place_id, user_id, data)
        return jsonify(review_schema.dump(review)), 201
    except ValidationError as err:
        logger.error(f"Validation Error: {err.messages}")
        abort(400, description=str(err.messages))

@reviews_bp.route("/places/<int:place_id>/reviews", methods=["GET"])
def get_reviews_for_place(place_id):
    reviews = get_reviews_from_place(place_id)
    return jsonify([review_schema.dump(review) for review in reviews]), 200

@reviews_bp.route("/users/<int:user_id>/reviews", methods=["GET"])
def get_user_reviews(user_id):
    reviews = get_reviews_from_user(user_id)
    return jsonify([review_schema.dump(review) for review in reviews]), 200

@reviews_bp.route("/", methods=["GET"])
def get_all_reviews():
    reviews = get_reviews()
    return jsonify([review_schema.dump(review) for review in reviews]), 200

@reviews_bp.route("/<int:review_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def review_operations(review_id):
    review = get_review_by_id(review_id)
    if not review:
        logger.warning(f"Review with id {review_id} not found")
        abort(404, description="Review not found")
    if request.method == "GET":
        return jsonify(review_schema.dump(review)), 200
    elif request.method == "PUT":
        try:
            data = review_schema.load(request.get_json())
            updated_review = update_review(review_id, data)
            return jsonify(review_schema.dump(updated_review)), 200
        except ValidationError as err:
            abort(400, description=str(err.messages))
    elif request.method == "DELETE":
        if delete_review(review_id):
            logger.info(f"Deleted review with id {review_id}")
            return '', 204
        else:
            logger.error(f"Failed to delete review with id {review_id}")
            abort(404, description="Review not found")

# Error handling and logging could be added here for specific statuses
@reviews_bp.errorhandler(404)
def handle_404(error):
    return jsonify({"error": "Not found", "message": str(error)}), 404

@reviews_bp.errorhandler(400)
def handle_400(error):
    return jsonify({"error": "Bad request", "message": str(error)}), 400

@reviews_bp.errorhandler(500)
def handle_500(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error", "message": str(error)}), 500


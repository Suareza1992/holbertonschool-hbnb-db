from flask import Blueprint, request, jsonify, abort
from src.controllers.users import create_user, delete_user, get_user_by_id, get_users, update_user
from marshmallow import Schema, fields, validate, ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the blueprint and limiter
users_bp = Blueprint("users", __name__, url_prefix="/users")
limiter = Limiter(key_func=get_remote_address)

# Define a schema for user data validation using Marshmallow
class UserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)

user_schema = UserSchema()

# Routes for user operations
@users_bp.route("/", methods=["GET"])
def get_all_users():
    users = get_users()
    return jsonify([user_schema.dump(user) for user in users]), 200

@users_bp.route("/", methods=["POST"])
@jwt_required()
@limiter.limit("5 per minute")
def create_new_user():
    json_data = request.get_json()
    try:
        data = user_schema.load(json_data)
        user = create_user(data)
        logger.info(f"User created: {data['username']}")
        return jsonify(user_schema.dump(user)), 201
    except ValidationError as err:
        logger.error("Validation error: {}".format(err.messages))
        abort(400, description=str(err.messages))

@users_bp.route("/<int:user_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def user_operations(user_id):
    user = get_user_by_id(user_id)
    if not user:
        logger.warning(f"User with id {user_id} not found")
        abort(404, description="User not found")

    if request.method == "GET":
        return jsonify(user_schema.dump(user)), 200
    elif request.method == "PUT":
        json_data = request.get_json()
        try:
            data = user_schema.load(json_data)
            updated_user = update_user(user_id, data)
            logger.info(f"User updated: {user_id}")
            return jsonify(user_schema.dump(updated_user)), 200
        except ValidationError as err:
            abort(400, description=str(err.messages))
    elif request.method == "DELETE":
        delete_user(user_id)
        logger.info(f"User deleted: {user_id}")
        return '', 204

# Error handling
@users_bp.errorhandler(404)
def handle_404(error):
    return jsonify({"error": "Resource not found", "message": str(error)}), 404

@users_bp.errorhandler(400)
def handle_400(error):
    return jsonify({"error": "Bad request", "message": str(error)}), 400

@users_bp.errorhandler(500)
def handle_500(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error", "message": str(error)}), 500

# Register the limiter with the blueprint
limiter.init_app(users_bp)


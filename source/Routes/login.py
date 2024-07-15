from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask extensions
jwt = JWTManager()  # Assume initialization in the main app config
limiter = Limiter(key_func=get_remote_address)

# Blueprint setup
login_bp = Blueprint("login", __name__, url_prefix="/login")
auth_bp = Blueprint("protected", __name__, url_prefix="/protected")

# Environment configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Rate limit for login attempts to prevent brute force attacks
@login_bp.route("/", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        abort(400, description="Missing username or password")
    if validate_credentials(username, password):  # Assuming validate_credentials is defined
        access_token = create_access_token(identity=username)
        logger.info(f"Successful login for user {username}")
        return jsonify(access_token=access_token), 200
    logger.warning(f"Failed login attempt for user {username}")
    return jsonify({"error": "Invalid credentials"}), 401

# Protected route requiring JWT for access
@auth_bp.route("/", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"data": "Secret data accessible only with valid JWT"}), 200

# Error handling for unauthorized access
@auth_bp.errorhandler(401)
def handle_unauthorized(e):
    return jsonify(error="Unauthorized access", description=str(e)), 401

# Initialize these blueprints and extensions in your main application setup
def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY  # Ensure the key is set in the environment
    jwt.init_app(app)
    limiter.init_app(app)
    app.register_blueprint(login_bp)
    app.register_blueprint(auth_bp)
    return app

# Dummy function to simulate credential validation
def validate_credentials(username, password):
    # Placeholder for your authentication logic
    return username == "admin" and password == "password"


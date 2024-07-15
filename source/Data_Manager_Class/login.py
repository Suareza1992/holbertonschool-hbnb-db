from flask import request, jsonify, abort
from src.models.user import User
from src import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import logging
from datetime import timedelta

# Setup logging
logger = logging.getLogger(__name__)

# Assuming configuration settings are imported from a config module
from config import Config

def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        abort(400, 'Email and password are required.')

    user = User.query.filter_by(email=email).first()
    if not user:
        logger.warning(f"Failed login attempt for nonexistent user: {email}")
        abort(401, 'User not found.')

    if not bcrypt.check_password_hash(user.password_hash, password):
        logger.warning(f"Failed login attempt for {email}: Incorrect password")
        abort(401, 'Wrong username or password.')

    additional_claims = {"is_admin": user.is_admin}
    access_token = create_access_token(
        identity=email, 
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    )
    return jsonify(access_token=access_token), 200

@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

def check_admin():
    claims = get_jwt()
    return claims.get('is_admin', False)


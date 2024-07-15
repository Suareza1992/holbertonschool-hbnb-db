from flask import Blueprint, jsonify, abort
from src.controllers.admin import admin_data_post, admin_data_delete
from flask_httpauth import HTTPBasicAuth

# Initialize Blueprint and HTTP Basic Authentication
admin_bp = Blueprint("admin", __name__, url_prefix="/admin/data")
auth = HTTPBasicAuth()

# Authentication function
@auth.verify_password
def verify_password(username, password):
    # Placeholder: replace with your actual user authentication logic
    return username == "admin" and password == "securepassword"

# Decorator to check if the user is authenticated and authorized
def require_admin(f):
    @auth.login_required
    def decorated_function(*args, **kwargs):
        if not auth.current_user() or not user_is_admin(auth.current_user()):
            abort(403, description="Access denied: You do not have permission to access this resource.")
        return f(*args, **kwargs)
    return decorated_function

# Route for updating administrative data
@admin_bp.route("/update", methods=["POST"])
@require_admin
def post_admin_data():
    """Handle POST requests to update administrative data."""
    return admin_data_post()

# Route for deleting administrative data
@admin_bp.route("/delete", methods=["DELETE"])
@require_admin
def delete_admin_data():
    """Handle DELETE requests to remove administrative data."""
    return admin_data_delete()

def user_is_admin(username):
    # Placeholder: replace with your actual check for administrative privileges
    return username == "admin"


from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

@jwt_required()
def admin_data():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

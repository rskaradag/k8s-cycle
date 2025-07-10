from flask import Blueprint, jsonify, request, Response
from app.models.user import User
from app.db.database import db
from datetime import datetime
import json

user_bp = Blueprint("user", __name__)

@user_bp.route("/api/users", methods=["GET"])
def get_resources():
    users = User.query.all()
    data = [u.to_dict() for u in users]
    json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    return Response(json_data, content_type="application/json; charset=utf-8")

@user_bp.route("/api/users/add", methods=["POST"])
def add_user():
    data = request.get_json()

    required_fields = ["username", "email"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "username and email are required"}), 400

    if User.query.filter((User.username == data["username"]) | (User.email == data["email"])).first():
        return jsonify({"error": "username or email already exists"}), 409

    new_user = User(
        username=data["username"],
        email=data["email"],
        full_name=data.get("full_name"), 
        created_at=datetime.utcnow()
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "created_at": new_user.created_at.isoformat()
        }
    }), 201
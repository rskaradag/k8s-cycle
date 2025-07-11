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

@user_bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200

@user_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

@user_bp.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "full_name" in data:
        user.full_name = data["full_name"]

    db.session.commit()

    return jsonify({
        "message": "User updated successfully",
        "user": user.to_dict()
    }), 200

@user_bp.route("/api/users/<int:user_id>/resources", methods=["GET"])
def get_user_resources(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    resources = user.resource_requests
    return jsonify([r.to_dict() for r in resources]), 200

@user_bp.route("/api/users/<int:user_id>/resources/<string:resource_id>", methods=["GET"])
def get_user_resource(user_id, resource_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    resource = next((r for r in user.resource_requests if r.resource_request_id == resource_id), None)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404

    return jsonify(resource.to_dict()), 200

@user_bp.route("/api/users/<int:user_id>/resources/<string:resource_id>", methods=["DELETE"])
def delete_user_resource(user_id, resource_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    resource = next((r for r in user.resource_requests if r.resource_request_id == resource_id), None)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404

    db.session.delete(resource)
    db.session.commit()

    return jsonify({"message": "Resource deleted successfully"}), 200

@user_bp.route("/api/users/<int:user_id>/resources/<string:resource_id>", methods=["PUT"])
def update_user_resource(user_id, resource_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    resource = next((r for r in user.resource_requests if r.resource_request_id == resource_id), None)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "request_name" in data:
        resource.request_name = data["request_name"]
    if "resource_url" in data:
        resource.resource_url = data["resource_url"]

    db.session.commit()

    return jsonify({
        "message": "Resource updated successfully",
        "resource": resource.to_dict()
    }), 200

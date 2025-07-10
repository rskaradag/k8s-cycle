from flask import Blueprint, jsonify
from app.models.resource_request import ResourceRequest

resource_bp = Blueprint("resource", __name__)

@resource_bp.route("/api/resources", methods=["GET"])
def get_resources():
    resources = ResourceRequest.query.all()
    return jsonify([r.to_dict() for r in resources])
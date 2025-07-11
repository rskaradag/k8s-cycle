from flask import Blueprint, jsonify, request
from app.models.resource_request import ResourceRequest
from datetime import datetime
from threading import Timer
import random, string
from app.db.database import db

resource_bp = Blueprint("resource", __name__)

def generate_request_id(length=10):
    return ''.join(random.choices(string.digits, k=length))

@resource_bp.route("/api/resources", methods=["GET"])
def get_resources():
    resource_id = request.args.get('id')

    if resource_id:
        resource = ResourceRequest.query.filter_by(resource_request_id=resource_id).first()
        if not resource:
            return jsonify({'error': 'Resource not found'}), 404
        return jsonify(resource.to_dict())

    resources = ResourceRequest.query.all()
    return jsonify([r.to_dict() for r in resources])

@resource_bp.route("/api/resources/create", methods=["POST"])
def create_resource():
    data = request.get_json()

    if not data.get('user_id') or not data.get('resource_url'):
        return jsonify({'error': 'user_id and resource_url are required'}), 400

    new_request = ResourceRequest(
        user_id=data['user_id'],
        resource_request_id=generate_request_id(),
        request_name=data.get('request_name', ''),
        resource_url=data['resource_url'],
        status='pending',
        created_at=datetime.utcnow()
    )

    db.session.add(new_request)
    db.session.commit()

    # mark_request_completed.apply_async(args=[new_request.id], countdown=600)

    return jsonify({
        'request_id': new_request.resource_request_id,
        'status': 'pending'
    }), 200
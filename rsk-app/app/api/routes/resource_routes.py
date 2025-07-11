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

@resource_bp.route("/api/resources/<string:resource_request_id>", methods=["GET"])
def get_resource_by_id(resource_request_id):
    resource = ResourceRequest.query.filter_by(resource_request_id=resource_request_id).first()
    if not resource:
        return jsonify({'error': 'Resource request not found'}), 404
    return jsonify(resource.to_dict())

@resource_bp.route("/api/resources/<string:resource_request_id>/status", methods=["GET"])
def get_resource_status(resource_request_id):
    resource = ResourceRequest.query.filter_by(resource_request_id=resource_request_id).first()
    if not resource:
        return jsonify({'error': 'Resource request not found'}), 404
    return jsonify({'status': resource.status})

@resource_bp.route("/api/resources/<string:resource_request_id>/cancel", methods=["POST"])
def cancel_resource_request(resource_request_id):
    resource = ResourceRequest.query.filter_by(resource_request_id=resource_request_id).first()
    if not resource:
        return jsonify({'error': 'Resource request not found'}), 404

    if resource.status in ['completed', 'cancelled']:
        return jsonify({'error': 'Cannot cancel a completed or already cancelled request'}), 400

    resource.status = 'cancelled'
    db.session.commit()

    return jsonify({'message': 'Resource request cancelled successfully', 'status': resource.status}), 200

@resource_bp.route("/api/resources/<string:resource_request_id>/complete", methods=["POST"])
def complete_resource_request(resource_request_id):
    resource = ResourceRequest.query.filter_by(resource_request_id=resource_request_id).first()
    if not resource:
        return jsonify({'error': 'Resource request not found'}), 404

    if resource.status != 'pending':
        return jsonify({'error': 'Cannot complete a request that is not pending'}), 400

    resource.status = 'completed'
    db.session.commit()

    return jsonify({'message': 'Resource request completed successfully', 'status': resource.status}), 200

@resource_bp.route("/api/resources/<string:resource_request_id>/delete", methods=["DELETE"])
def delete_resource_request(resource_request_id):
    resource = ResourceRequest.query.filter_by(resource_request_id=resource_request_id).first()
    if not resource:
        return jsonify({'error': 'Resource request not found'}), 404

    db.session.delete(resource)
    db.session.commit()

    return jsonify({'message': 'Resource request deleted successfully'}), 200

@resource_bp.route("/api/resources/<string:resource_request_id>/update", methods=["PUT"])
def update_resource_request(resource_request_id):
    resource = ResourceRequest.query.filter_by(resource_request_id=resource_request_id).first()
    if not resource:
        return jsonify({'error': 'Resource request not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'request_name' in data:
        resource.request_name = data['request_name']
    if 'resource_url' in data:
        resource.resource_url = data['resource_url']

    db.session.commit()

    return jsonify({'message': 'Resource request updated successfully', 'resource': resource.to_dict()}), 200
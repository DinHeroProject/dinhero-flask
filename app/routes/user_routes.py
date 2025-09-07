from flask import Blueprint, request, jsonify
from app.services.user_service import *
from app.utils.errors import errors

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
def get_all():
    users, error = get_all_users()
    return jsonify(users), 200

@user_routes.route('/users', methods=['POST'])
def create():
    data = request.get_json()
    user, error = create_user(data)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(user), 201

@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get(user_id):
    user, error = get_user_by_id(user_id)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(user.to_dict()), 200

@user_routes.route('/users/<int:user_id>', methods=['PUT'])
def update(user_id):
    data = request.get_json()
    user, error = update_user_info(user_id, data)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(user), 200

@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    user, error = delete_user(user_id)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(user), 200

@user_routes.route('/users/<int:user_id>/profile', methods=['PUT'])
def profile_update(user_id):
    profile_data = request.get_json()
    user, error = update_profile(user_id, profile_data)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(user), 200

@user_routes.route('/users/<int:user_id>/profile', methods=['GET'])
def get_profile(user_id):
    profile, error = get_user_profile(user_id)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(profile), 200
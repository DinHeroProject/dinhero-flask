from flask import Blueprint, request, jsonify
from app.services.mentorship_service import *
from app.utils.errors import errors

mentorship_routes = Blueprint('mentorship_routes', __name__)

@mentorship_routes.route('/mentorships', methods=['POST'])
def create():
    data = request.json
    mentorship, error = create_mentorship(data)
    if error:
        return jsonify({"error": errors[error]}), 400
    return jsonify(mentorship), 201

@mentorship_routes.route('/mentorships/<int:mentorship_id>', methods=['GET'])
def get_by_id(mentorship_id):
    mentorship, error = get_mentorship_by_id(mentorship_id)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(mentorship.to_dict()), 200

@mentorship_routes.route('/mentorships', methods=['GET'])
def get_all():
    mentorships, error = get_all_mentorships()
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(mentorships), 200

@mentorship_routes.route('/mentorships/<int:mentorship_id>', methods=['PUT'])
def update(mentorship_id):
    data = request.json
    mentorship, error = update_mentorship(mentorship_id, data)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(mentorship), 200

@mentorship_routes.route('/mentorships/<int:mentorship_id>', methods=['DELETE'])
def delete(mentorship_id):
    mentorship, error = delete_mentorship(mentorship_id)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(mentorship), 200

@mentorship_routes.route('/mentorships/mentor/<int:mentor_id>', methods=['GET'])
def get_by_mentor(mentor_id):
    mentorships, erro = get_mentorships_by_mentor(mentor_id)
    if erro:
        error_info = errors.get(erro, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(mentorships), 200

@mentorship_routes.route('/mentorships/aluno/<int:aluno_id>', methods=['GET'])
def get_by_aluno(aluno_id):
    mentorships, erro = get_mentorships_by_aluno(aluno_id)
    if erro:
        error_info = errors.get(erro, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(mentorships), 200
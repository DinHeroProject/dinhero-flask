from flask import Blueprint, request, jsonify
from services.course_services import *
from utils.errors import errors

course_routes = Blueprint('course_routes', __name__)

@course_routes.route('/courses', methods=['POST'])
def create():
    data = request.json
    course, error = create_course(data)
    if error:
        return jsonify({"error": errors[error]}), 400
    return jsonify(course), 201

@course_routes.route('/courses/<int:course_id>', methods=['GET'])
def get_by_id(course_id):
    course, error = get_course_by_id(course_id)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(course.to_dict()), 200

@course_routes.route('/courses', methods=['GET'])
def get_all():
    courses, error = get_all_courses()
    return jsonify(courses), 200

@course_routes.route('/courses/<int:course_id>', methods=['PUT'])
def update(course_id):
    data = request.json
    course, error = update_course(course_id, data)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(course), 200

@course_routes.route('/courses/<int:course_id>', methods=['DELETE'])
def delete(course_id):
    course, error = delete_course(course_id)
    if error:
        error_info = errors.get(error, {"mensagem": "Erro desconhecido", "status_code": 500})
        return jsonify({"mensagem": error_info["mensagem"]}), error_info["status_code"]

    return jsonify(course), 200
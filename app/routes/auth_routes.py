from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import *
from app.utils.errors import errors

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = AuthService.register_user(
            cpf=data['cpf'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        return jsonify({
            'id': user.id,
            'cpf': user.cpf,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }), 201
    except ValueError as e:
        error_type = str(e).split('(')[0]
        return jsonify(errors[error_type]), 400
    
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        user = AuthService.login_user(
            email=data['email'],
            password=data['password']
        )
        return jsonify({
            'token': user
        }), 200
    except ValueError as e:
        error_type = str(e).split('(')[0]
        return jsonify(errors[error_type]), 401

@auth_routes.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'User logged out successfully'}), 200

@auth_routes.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        
        user = AuthService.get_current_user(current_user_id)
        
        return jsonify({
            'id': user.id,
            'cpf': user.cpf,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'last_login': user.last_login
        }), 200
    except ValueError as e:
        error_type = str(e).split('(')[0]
        return jsonify(errors[error_type]), 404
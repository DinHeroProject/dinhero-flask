from flask import Blueprint, request, jsonify 

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Aqui você pode adicionar a lógica de registro

    return jsonify({"message": "Registration successful"}), 201

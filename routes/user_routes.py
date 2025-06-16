from flask import Blueprint, request, jsonify

user_routes = Blueprint('user_routes', __name__)




@user_routes.route('/users', methods=['GET'])
def get_users():
    pass
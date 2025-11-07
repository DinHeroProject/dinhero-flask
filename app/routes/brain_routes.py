from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.brain_service import chat_with_brain, get_welcome_message

brain_routes = Blueprint('brain', __name__)


@brain_routes.route('/brain/welcome', methods=['GET'])
@jwt_required()
def welcome():
    try:
        message = get_welcome_message()
        return jsonify(message), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@brain_routes.route('/brain/chat', methods=['POST'])
@jwt_required()
def chat():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Mensagem é obrigatória'}), 400
        
        message = data['message']
        history = data.get('history', [])
        
        # user_id = get_jwt_identity()
        
        result = chat_with_brain(message, history)
        
        if result['success']:
            return jsonify({
                'role': 'assistant',
                'content': result['response'],
                'model': result['model']
            }), 200
        else:
            return jsonify({
                'role': 'assistant',
                'content': result['response'],
                'error': result.get('error')
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

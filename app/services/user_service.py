from app.models.user import User
from app.dao.user_dao import UserDAO
from app.dao.profile_dao import ProfileDAO
import datetime
import re

def validate_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if (len(cpf) != 11) or (len(set(cpf)) == 1):
        return False
    for i in range(9, 11):
        soma = 0
        for j in range(i):
            soma += int(cpf[j]) * ((i + 1) - j)
        resto = soma % 11
        digito_verificador = 0 if resto < 2 else 11 - resto
        if int(cpf[i]) != digito_verificador:
            return False
    return True

def create_user(data):
    users = UserDAO.get_all()
    for user in users:
        if user.cpf == data.get('cpf'):
            return None, "CPF_ALREADY_EXISTS"
        if user.email == data.get('email'):
            return None, "EMAIL_ALREADY_EXISTS"
    if not data.get('cpf') or not data.get('email') or not data.get('password') or not data.get('first_name') or not data.get('last_name'):
        return None, "MISSING_REQUIRED_FIELD"
    if len(data.get('password', '')) < 6:
        return None, "INVALID_PASSWORD"
    if '@' not in data.get('email', '') or '.' not in data.get('email', ''):
        return None, "INVALID_EMAIL"
    if not validate_cpf(data.get('cpf', '')):
        return None, "INVALID_CPF"
    new_user = User(
        id=None,
        cpf=data.get('cpf'),
        email=data.get('email'),
        password=data.get('password'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
    )
    created = UserDAO.create(new_user)
    return created.to_dict(), None

def get_all_users():
    users = UserDAO.get_all()
    return [user.to_dict() for user in users], None

def get_user_by_id(user_id):
    try:
        user = UserDAO.get_by_id(user_id)
        return user, None
    except Exception:
        return None, "USER_NOT_FOUND"
    
def get_user_by_email(email):
    user = UserDAO.get_by_email(email)
    if user:
        return user, None
    else:
        return None, "USER_NOT_FOUND"

def update_user_info(user_id, data):
    try:
        user = UserDAO.get_by_id(user_id)
    except Exception:
        return None, "USER_NOT_FOUND"
    if not data:
        return None, "MISSING_REQUIRED_FIELD"

    users = UserDAO.get_all()
    for other_user in users:
        if other_user.id != user_id:
            if 'cpf' in data and other_user.cpf == data['cpf']:
                return None, "CPF_ALREADY_EXISTS"
            if 'email' in data and other_user.email == data['email']:
                return None, "EMAIL_ALREADY_EXISTS"

    if 'password' in data and len(data['password']) < 6:
        return None, "INVALID_PASSWORD"
    if 'email' in data:
        if '@' not in data['email'] or '.' not in data['email']:
            return None, "INVALID_EMAIL"
    if 'cpf' in data:
        if not validate_cpf(data['cpf']):
            return None, "INVALID_CPF"

    if 'cpf' in data:
        user.cpf = data['cpf']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']

    user.updated_at = datetime.datetime.now().isoformat()
    updated = UserDAO.update(user)
    return updated.to_dict(), None

def delete_user(user_id):
    try:
        UserDAO.delete(user_id)
        return {"mensagem": "Usuário deletado com sucesso."}, None
    except Exception:
        return None, "USER_NOT_FOUND"

def get_user_profile(user_id):
    """Retorna o perfil de um usuário"""
    user, error = get_user_by_id(user_id)
    if error:
        return None, error
    return user.profile, None

def validate_profile_data(profile_data):
    """Valida os dados do perfil"""
    errors = []
    
    # Validação de data de nascimento
    if 'date_of_birth' in profile_data and profile_data['date_of_birth']:
        date_str = profile_data['date_of_birth']
        # Aceita formatos: YYYY-MM-DD, DD/MM/YYYY
        date_pattern1 = r'^\d{4}-\d{2}-\d{2}$'
        date_pattern2 = r'^\d{2}/\d{2}/\d{4}$'
        
        if not (re.match(date_pattern1, date_str) or re.match(date_pattern2, date_str)):
            errors.append("Data de nascimento deve estar no formato YYYY-MM-DD ou DD/MM/YYYY")
        else:
            try:
                if re.match(date_pattern2, date_str):
                    # Converte DD/MM/YYYY para YYYY-MM-DD
                    day, month, year = date_str.split('/')
                    profile_data['date_of_birth'] = f"{year}-{month}-{day}"
                
                # Valida se é uma data válida
                datetime.datetime.strptime(profile_data['date_of_birth'], '%Y-%m-%d')
            except ValueError:
                errors.append("Data de nascimento inválida")
    
    # Validação de gênero
    if 'gender' in profile_data and profile_data['gender']:
        valid_genders = ['male', 'female', 'other', 'prefer_not_to_say']
        if profile_data['gender'].lower() not in valid_genders:
            errors.append("Gênero inválido")
    
    # Validação de preferência de idioma
    if 'language_preference' in profile_data and profile_data['language_preference']:
        valid_languages = ['pt-br', 'en', 'es', 'fr', 'de', 'it', 'pt', 'portuguese', 'english', 'spanish']
        if profile_data['language_preference'].lower() not in valid_languages:
            errors.append("Idioma inválido")
    
    # Validação de estilo de aprendizagem
    if 'learning_style_preference' in profile_data and profile_data['learning_style_preference']:
        valid_styles = ['visual', 'auditory', 'kinesthetic', 'reading_writing']
        if profile_data['learning_style_preference'].lower() not in valid_styles:
            errors.append("Estilo de aprendizagem inválido")
    
    # Validação de complexidade de conteúdo
    if 'content_complexity_preference' in profile_data and profile_data['content_complexity_preference']:
        valid_complexity = ['basic', 'intermediate', 'advanced']
        if profile_data['content_complexity_preference'].lower() not in valid_complexity:
            errors.append("Preferência de complexidade inválida")
    
    # Validação de preferência de duração de vídeo
    if 'video_length_preference' in profile_data and profile_data['video_length_preference']:
        valid_lengths = ['short', 'medium', 'long']
        if profile_data['video_length_preference'].lower() not in valid_lengths:
            errors.append("Preferência de duração de vídeo inválida")
    
    # Validação de URL do avatar
    if 'avatar_url' in profile_data and profile_data['avatar_url']:
        url_pattern = r'^https?://.+'
        if not re.match(url_pattern, profile_data['avatar_url']):
            errors.append("URL do avatar inválida")
    
    # Validação de bio (limite de caracteres)
    if 'bio' in profile_data and profile_data['bio']:
        if len(profile_data['bio']) > 500:
            errors.append("Bio não pode ter mais de 500 caracteres")
    
    return errors if errors else None

def update_profile(user_id, profile_data):
    """Atualiza o perfil de um usuário"""
    user, error = get_user_by_id(user_id)
    if error:
        return None, error
    
    if not profile_data:
        return None, "MISSING_REQUIRED_FIELD"
    
    # Valida os dados do perfil
    validation_errors = validate_profile_data(profile_data)
    if validation_errors:
        return None, {"errors": validation_errors, "code": "INVALID_PROFILE_DATA"}
    
    try:
        # Atualiza o perfil no banco de dados
        updated_profile = ProfileDAO.update(user_id, profile_data)
        
        # Atualiza o timestamp do usuário
        user.updated_at = datetime.datetime.now().isoformat()
        UserDAO.update(user)
        
        # Retorna o usuário atualizado com o novo perfil
        user, _ = get_user_by_id(user_id)
        return user.to_dict(), None
    except Exception as e:
        return None, "PROFILE_UPDATE_ERROR"
from app.models.user import User
from app.dao.user_dao import UserDAO
import datetime

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
    user, error = get_user_by_id(user_id)
    if error:
        return None, error
    return user.profile, None

def update_profile(user_id, profile_data):
    user, error = get_user_by_id(user_id)
    if error:
        return None, error
    if not profile_data:
        return None, "MISSING_REQUIRED_FIELD"
    user.profile.update(profile_data)
    user.updated_at = datetime.datetime.now().isoformat()
    updated = UserDAO.update(user)
    return updated.to_dict(), None
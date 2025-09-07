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

def update_user_info(user_id, data):
    users = UserDAO.get_all()
    for user in users:
        if user.id != user_id:
            if user.cpf == data.get('cpf'):
                return None, "CPF_ALREADY_EXISTS"
            if user.email == data.get('email'):
                return None, "EMAIL_ALREADY_EXISTS"
    try:
        user = UserDAO.get_by_id(user_id)
    except Exception:
        return None, "USER_NOT_FOUND"
    if not data:
        return None, "MISSING_REQUIRED_FIELD"
    if len(data.get('password', '')) < 6:
        return None, "INVALID_PASSWORD"
    if '@' not in data.get('email', '') or '.' not in data.get('email', ''):
        return None, "INVALID_EMAIL"
    if not validate_cpf(data.get('cpf', '')):
        return None, "INVALID_CPF"
    user.cpf = data.get('cpf', user.cpf)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
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
from models.user import User
import datetime

users = []


# ------------------- UTILITIES -------------------

def generate_user_id():
    if not users:
        return 1
    return max(user.id for user in users) + 1

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

# -------------------------------------------------

def create_user(data):
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
        id=generate_user_id(),
        cpf=data.get('cpf'),
        email=data.get('email'),
        password=data.get('password'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
    )
    users.append(new_user)
    return new_user.to_dict(), None

def get_all_users():
    return [user.to_dict() for user in users], None

def get_user_by_id(user_id):
    for user in users:
        if user.id == user_id:
            return user, None
    return None, "USER_NOT_FOUND"

def update_user_info(user_id, data):
    for user in users:
        if user.id != user_id:
            if user.cpf == data.get('cpf'):
                return None, "CPF_ALREADY_EXISTS"
            if user.email == data.get('email'):
                return None, "EMAIL_ALREADY_EXISTS"
    for user in users:
        if user.id == user_id:
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
            return user.to_dict(), None
    return None, "USER_NOT_FOUND"

def delete_user(user_id):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"mensagem": "Usuário deletado com sucesso."}, None
    return None, "USER_NOT_FOUND"

def get_user_profile(user_id):
    target_user, error = get_user_by_id(user_id)
    if error:
        return None, error
    if target_user.profile:
        users.remove(target_user)
        return target_user.profile, None

def update_profile(user_id, profile_data):
    target_user, error = get_user_by_id(user_id)
    if error:
        return None, error
    
    if not profile_data:
        return None, "MISSING_REQUIRED_FIELD"
    
    target_user.profile.update(profile_data)
    target_user.updated_at = datetime.datetime.now().isoformat()
    
    return target_user.to_dict(), None
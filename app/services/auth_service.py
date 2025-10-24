from flask_jwt_extended import create_access_token
from app.models.user import User
from app.dao.user_dao import UserDAO
import datetime
import bcrypt



class AuthService:
    @staticmethod
    def register_user(cpf: str, email: str, password: str, first_name: str, last_name: str) -> User:
        existing_users = UserDAO.get_all()
        if any(u.email == email for u in existing_users):
            raise ValueError('USER_ALREADY_EXISTS')('User with this email already exists')
        if any(u.cpf == cpf for u in existing_users):
            raise ValueError('USER_ALREADY_EXISTS')('User with this CPF already exists')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = User(
            id=None,
            cpf=cpf,
            email=email,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
        )
        created_user = UserDAO.create(new_user)
        return created_user

    @staticmethod
    def login_user(email: str, password: str) -> User:
        user = UserDAO.get_by_email(email)
        if not user:
            raise ValueError('INVALID_CREDENTIALS')('Invalid email or password')

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise ValueError('INVALID_CREDENTIALS')('Invalid email or password')
        else:
            token = create_access_token(identity=user.id)

            user.last_login = datetime.datetime.now()
            UserDAO.update(user)

        return token
    
    @staticmethod
    def logout_user():
        return True
    
    @staticmethod
    def get_current_user(user_id: int) -> User:
        user = UserDAO.get_by_id(user_id)
        if not user:
            raise ValueError('RESOURCE_NOT_FOUND')('User not found')
        return user
import os
import sqlite3
from app.models.user import User

DB_PATH = os.getenv('DATABASE_URL')

class UserDAO:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def create_table():
        with UserDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite não tem suporte ao tipo SERIAL, alterar para produção
                    cpf VARCHAR(14) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            conn.commit()

    @staticmethod
    def create(user: User):
        with UserDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (cpf, email, password, first_name, last_name) VALUES (?, ?, ?, ?, ?)', (user.cpf, user.email, user.password, user.first_name, user.last_name))
            conn.commit()
            user.id = cursor.lastrowid
            return user

    @staticmethod
    def get_by_id(user_id: int):
        with UserDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, cpf, first_name, last_name, email, password FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                return User(id=row[0], cpf=row[1], first_name=row[2], last_name=row[3], email=row[4], password=row[5])
            else:
                raise ValueError('RESOURCE_NOT_FOUND')('User not found')

    @staticmethod
    def get_all():
        with UserDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, cpf, first_name, last_name, email, password FROM users')
            rows = cursor.fetchall()
            return [User(id=row[0], cpf=row[1], first_name=row[2], last_name=row[3], email=row[4], password=row[5]) for row in rows]

    @staticmethod
    def update(user: User):
        with UserDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET first_name = ?, last_name = ?, email = ? WHERE id = ?', (user.first_name, user.last_name, user.email, user.id))
            conn.commit()
            if cursor.rowcount == 0:
                raise ValueError('RESOURCE_NOT_FOUND')('User not found')
            return user

    @staticmethod
    def delete(user_id: int):
        with UserDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise ValueError('RESOURCE_NOT_FOUND')('User not found')

import os
import sqlite3
import json

DB_PATH = os.getenv('DATABASE_URL')

class ProfileDAO:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def create_table():
        with ProfileDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id INTEGER PRIMARY KEY,
                    avatar_url TEXT,
                    bio TEXT,
                    date_of_birth DATE,
                    gender VARCHAR(50),
                    country VARCHAR(100),
                    language_preference VARCHAR(50),
                    learning_style_preference VARCHAR(100),
                    content_complexity_preference VARCHAR(50),
                    video_length_preference VARCHAR(50),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            conn.commit()

    @staticmethod
    def create(user_id: int, profile_data: dict):
        """Cria um perfil para um usuário"""
        with ProfileDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_profiles (
                    user_id, avatar_url, bio, date_of_birth, gender, country,
                    language_preference, learning_style_preference,
                    content_complexity_preference, video_length_preference
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                profile_data.get('avatar_url'),
                profile_data.get('bio'),
                profile_data.get('date_of_birth'),
                profile_data.get('gender'),
                profile_data.get('country'),
                profile_data.get('language_preference'),
                profile_data.get('learning_style_preference'),
                profile_data.get('content_complexity_preference'),
                profile_data.get('video_length_preference')
            ))
            conn.commit()
            return ProfileDAO.get_by_user_id(user_id)

    @staticmethod
    def get_by_user_id(user_id: int):
        """Busca o perfil de um usuário"""
        with ProfileDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, avatar_url, bio, date_of_birth, gender, country,
                       language_preference, learning_style_preference,
                       content_complexity_preference, video_length_preference,
                       created_at, updated_at
                FROM user_profiles
                WHERE user_id = ?
            ''', (user_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'user_id': row[0],
                    'avatar_url': row[1],
                    'bio': row[2],
                    'date_of_birth': row[3],
                    'gender': row[4],
                    'country': row[5],
                    'language_preference': row[6],
                    'learning_style_preference': row[7],
                    'content_complexity_preference': row[8],
                    'video_length_preference': row[9],
                    'created_at': row[10],
                    'updated_at': row[11]
                }
            return None

    @staticmethod
    def update(user_id: int, profile_data: dict):
        """Atualiza o perfil de um usuário"""
        with ProfileDAO.get_connection() as conn:
            cursor = conn.cursor()
            
            # Verifica se o perfil existe
            existing = ProfileDAO.get_by_user_id(user_id)
            if not existing:
                # Se não existe, cria um novo
                return ProfileDAO.create(user_id, profile_data)
            
            # Monta a query de atualização dinamicamente
            update_fields = []
            values = []
            
            allowed_fields = [
                'avatar_url', 'bio', 'date_of_birth', 'gender', 'country',
                'language_preference', 'learning_style_preference',
                'content_complexity_preference', 'video_length_preference'
            ]
            
            for field in allowed_fields:
                if field in profile_data:
                    update_fields.append(f"{field} = ?")
                    values.append(profile_data[field])
            
            if not update_fields:
                return existing
            
            # Adiciona o updated_at
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(user_id)
            
            query = f"UPDATE user_profiles SET {', '.join(update_fields)} WHERE user_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise ValueError('Profile not found')
            
            return ProfileDAO.get_by_user_id(user_id)

    @staticmethod
    def delete(user_id: int):
        """Deleta o perfil de um usuário"""
        with ProfileDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user_profiles WHERE user_id = ?', (user_id,))
            conn.commit()
            return cursor.rowcount > 0

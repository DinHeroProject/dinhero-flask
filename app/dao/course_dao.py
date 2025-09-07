import os
import sqlite3
from app.models.course import Course

DB_PATH = os.getenv('DATABASE_URL')

class CourseDAO:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def create_table():
        with CourseDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    category VARCHAR(100),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    author_id INT NOT NULL,
                    difficulty_level VARCHAR(50),
                    estimated_duration_minutes INT,
                    thumbnail_url VARCHAR(500),
                    is_private BOOLEAN DEFAULT FALSE,
                    language VARCHAR(50),
                    number_of_modules INT,
                    rating DECIMAL(3,2),  -- ex: 4.75
                    reviews INT DEFAULT 0,
                    CONSTRAINT fk_author FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            conn.commit()

    @staticmethod
    def create(course: Course):
        with CourseDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO courses (title, description, category, author_id, difficulty_level, estimated_duration_minutes, thumbnail_url, is_private, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (course.title, course.description, course.category, course.author_id, course.difficulty_level, course.estimated_duration_minutes, course.thumbnail_url, course.is_private, course.language))
            conn.commit()
            course.id = cursor.lastrowid
            return course

    @staticmethod
    def get_by_id(course_id: int):
        with CourseDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, description, category, author_id, difficulty_level, estimated_duration_minutes, thumbnail_url, is_private, language, number_of_modules, rating FROM courses WHERE id = ?', (course_id,))
            row = cursor.fetchone()
            if row:
                return Course(id=row[0], title=row[1], description=row[2], category=row[3], author_id=row[4], difficulty_level=row[5], estimated_duration_minutes=row[6], thumbnail_url=row[7], is_private=row[8], language=row[9])
            else:
                raise ValueError('RESOURCE_NOT_FOUND')

    @staticmethod
    def get_all():
        with CourseDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, description, category, author_id, difficulty_level, estimated_duration_minutes, thumbnail_url, is_private, language, number_of_modules, rating FROM courses')
            rows = cursor.fetchall()
            return [Course(id=row[0], title=row[1], description=row[2], category=row[3], author_id=row[4], difficulty_level=row[5], estimated_duration_minutes=row[6], thumbnail_url=row[7], is_private=row[8], language=row[9]) for row in rows]

    @staticmethod
    def get_by_user(user_id: int):
        with CourseDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, description, category, author_id, difficulty_level, estimated_duration_minutes, thumbnail_url, is_private, language, number_of_modules, rating FROM courses WHERE author_id = ?', (user_id,))
            rows = cursor.fetchall()
            return [Course(id=row[0], title=row[1], description=row[2], category=row[3], author_id=row[4], difficulty_level=row[5], estimated_duration_minutes=row[6], thumbnail_url=row[7], is_private=row[8], language=row[9]) for row in rows]

    @staticmethod
    def update(course: Course):
        with CourseDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE courses SET title = ?, description = ?, category = ?, author_id = ?, difficulty_level = ?, estimated_duration_minutes = ?, thumbnail_url = ?, is_private = ?, language = ?, number_of_modules = ?, rating = ? WHERE id = ?', (course.title, course.description, course.category, course.author_id, course.difficulty_level, course.estimated_duration_minutes, course.thumbnail_url, course.is_private, course.language, course.number_of_modules, course.rating, course.id))
            conn.commit()
            if cursor.rowcount == 0:
                raise ValueError('RESOURCE_NOT_FOUND')
            return course

    @staticmethod
    def delete(course_id: int):
        with CourseDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise ValueError('RESOURCE_NOT_FOUND')

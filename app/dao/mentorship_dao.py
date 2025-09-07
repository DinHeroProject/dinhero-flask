import os
import sqlite3
from app.models.mentorship import Mentorship

DB_PATH = os.getenv('DATABASE_URL')

class MentorshipDAO:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def create_table():
        with MentorshipDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mentorships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mentor_id INT NOT NULL,
                    aluno_id INT NOT NULL,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP,
                    status VARCHAR(50) NOT NULL,
                    topic VARCHAR(255),
                    meet_type VARCHAR(50),
                    notes TEXT,
                    aluno_feedback TEXT,
                    mentor_feedback TEXT,
                    CONSTRAINT fk_mentor FOREIGN KEY (mentor_id) REFERENCES users (id) ON DELETE CASCADE,
                    CONSTRAINT fk_aluno FOREIGN KEY (aluno_id) REFERENCES users (id) ON DELETE CASCADE
                );
            ''')
            conn.commit()

    @staticmethod
    def create(mentorship: Mentorship):
        with MentorshipDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO mentorships (title, description, mentor_id) VALUES (?, ?, ?)', (mentorship.title, mentorship.description, mentorship.mentor_id))
            conn.commit()
            mentorship.id = cursor.lastrowid
            return mentorship

    @staticmethod
    def get_by_id(mentorship_id: int):
        with MentorshipDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, description, mentor_id FROM mentorships WHERE id = ?', (mentorship_id,))
            row = cursor.fetchone()
            if row:
                return Mentorship(id=row[0], title=row[1], description=row[2], mentor_id=row[3])
            else:
                raise ValueError('RESOURCE_NOT_FOUND')

    @staticmethod
    def get_all():
        with MentorshipDAO.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, description, mentor_id FROM mentorships')
            rows = cursor.fetchall()
            return [Mentorship(id=row[0], title=row[1], description=row[2], mentor_id=row[3]) for row in rows]
import os
import sqlite3
from app.dao.mentorship_dao import MentorshipDAO
from app.dao.user_dao import UserDAO
from app.dao.course_dao import CourseDAO

DB_PATH = os.getenv('DATABASE_URL')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        pass
    UserDAO.create_table()
    CourseDAO.create_table()
    MentorshipDAO.create_table()
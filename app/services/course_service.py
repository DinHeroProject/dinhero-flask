from app.models.course import Course
from app.dao.course_dao import CourseDAO
import datetime

def create_course(data):
    if not data.get('title') or not data.get('description') or not data.get('category') or not data.get('author_id'):
        return None, "MISSING_REQUIRED_FIELD"
    new_course = Course(
        id=None,
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        author_id=data.get('author_id'),
        difficulty_level=data.get('difficulty_level', None),
        estimated_duration_minutes=data.get('estimated_duration_minutes', 0),
        thumbnail_url=data.get('thumbnail_url', None),
        is_private=data.get('is_private', False),
        language=data.get('language', 'pt-BR')
    )
    created = CourseDAO.create(new_course)
    return created.to_dict(), None

def get_course_by_id(course_id):
    try:
        course = CourseDAO.get_by_id(course_id)
        return course, None
    except Exception:
        return None, "RESOURCE_NOT_FOUND"

def get_all_courses():
    courses = CourseDAO.get_all()
    return [course.to_dict() for course in courses], None

def update_course(course_id, data):
    try:
        course = CourseDAO.get_by_id(course_id)
    except Exception:
        return None, "RESOURCE_NOT_FOUND"
    course.title = data.get('title', course.title)
    course.description = data.get('description', course.description)
    course.category = data.get('category', course.category)
    course.author_id = data.get('author_id', course.author_id)
    course.difficulty_level = data.get('difficulty_level', course.difficulty_level)
    course.estimated_duration_minutes = data.get('estimated_duration_minutes', course.estimated_duration_minutes)
    course.thumbnail_url = data.get('thumbnail_url', course.thumbnail_url)
    course.is_private = data.get('is_private', course.is_private)
    course.language = data.get('language', course.language)
    course.number_of_modules = data.get('number_of_modules', course.number_of_modules)
    course.rating = data.get('rating', course.rating)
    course.reviews = data.get('reviews', course.reviews)
    course.updated_at = datetime.datetime.now().isoformat()
    updated = CourseDAO.update(course)
    return updated.to_dict(), None

def delete_course(course_id):
    try:
        CourseDAO.delete(course_id)
        return {"mensagem": "Curso deletado com sucesso."}, None
    except Exception:
        return None, "RESOURCE_NOT_FOUND"

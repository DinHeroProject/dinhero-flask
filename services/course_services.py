from models.course import Course
import datetime

courses = []


# ------------------- UTILITIES -------------------

def generate_course_id():
    if not courses:
        return 1
    return max(course.id for course in courses) + 1

# -------------------------------------------------

def create_course(data):
    if not data.get('title') or not data.get('description') or not data.get('category') or not data.get('author_id'):
        return None, "MISSING_REQUIRED_FIELD"
    
    new_course = Course(
        id=generate_course_id(),
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        author_id=data.get('author_id'),
        difficulty_level=data.get('difficulty_level', None),
        estimated_duration_minutes=data.get('estimated_duration_minutes', 0),
        thumbnail_url=data.get('thumbnail_url', None),
        is_private=data.get('is_private', False),
        language=data.get('language', []),
        number_of_modules=data.get('number_of_modules', 0),
        rating=data.get('rating', 0.0),
        reviews=data.get('reviews', [])
    )
    courses.append(new_course)
    return new_course.to_dict(), None

def get_course_by_id(target_id):
    for course in courses:
        if course.id == target_id:
            return course, None
    return None, "RESOURCE_NOT_FOUND"

def get_all_courses():
    return [course.to_dict() for course in courses], None

def update_course(course_id, data):
    course, error = get_course_by_id(course_id)
    if error:
        return None, error
    
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
    course.updated_at = datetime.datetime.now()
    
    return course.to_dict(), None

def delete_course(course_id):
    course, error = get_course_by_id(course_id)
    if error:
        return None, error
    
    courses.remove(course)
    return course.to_dict(), None

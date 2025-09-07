from ..models.mentorship import Mentorship
import datetime

mentorships = []


# ------------------- UTILITIES -------------------

def generate_mentorship_id():
    if not mentorships:
        return 1
    return max(mentorship.id for mentorship in mentorships) + 1

# -------------------------------------------------

def create_mentorship(data):
    if not data.get('mentor_id') or not data.get('aluno_id') or not data.get('start_time') or not data.get('end_time'):
        return None, "MISSING_REQUIRED_FIELD"
    
    new_mentorship = Mentorship(
        id=generate_mentorship_id(),
        mentor_id=data.get('mentor_id'),
        aluno_id=data.get('aluno_id'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        status=data.get('status', 'pending'),
        topic=data.get('topic', ''),
        meet_type=data.get('meet_type', 'video'),
        notes=data.get('notes', ''),
        aluno_feedback=data.get('aluno_feedback', ''),
        mentor_feedback=data.get('mentor_feedback', ''),
    )
    mentorships.append(new_mentorship)
    return new_mentorship.to_dict(), None

def get_mentorship_by_id(target_id):
    for mentorship in mentorships:
        if mentorship.id == target_id:
            return mentorship, None
    return None, "RESOURCE_NOT_FOUND"

def get_all_mentorships():
    return [mentorship.to_dict() for mentorship in mentorships], None

def update_mentorship(mentorship_id, data):
    mentorship, error = get_mentorship_by_id(mentorship_id)
    if error:
        return None, error
    
    mentorship.mentor_id = data.get('mentor_id', mentorship.mentor_id)
    mentorship.aluno_id = data.get('aluno_id', mentorship.aluno_id)
    mentorship.start_time = data.get('start_time', mentorship.start_time)
    mentorship.end_time = data.get('end_time', mentorship.end_time)
    mentorship.status = data.get('status', mentorship.status)
    mentorship.topic = data.get('topic', mentorship.topic)
    mentorship.meet_type = data.get('meet_type', mentorship.meet_type)
    mentorship.notes = data.get('notes', mentorship.notes)
    mentorship.aluno_feedback = data.get('aluno_feedback', mentorship.aluno_feedback)
    mentorship.mentor_feedback = data.get('mentor_feedback', mentorship.mentor_feedback)

    return mentorship.to_dict(), None

def delete_mentorship(mentorship_id):
    targert_mentorship, error = get_mentorship_by_id(mentorship_id)
    if error:
        return None, error
    else:
        mentorships.remove(targert_mentorship)
        return targert_mentorship.to_dict(), None

def get_mentorships_by_mentor(mentor_id):
    mentor_mentorships = [mentorship.to_dict() for mentorship in mentorships if mentorship.mentor_id == mentor_id]
    if not mentor_mentorships:
        return None, "USER_NOT_FOUND"
    return mentor_mentorships, None

def get_mentorships_by_aluno(aluno_id):
    aluno_mentorships = [mentorship.to_dict() for mentorship in mentorships if mentorship.aluno_id == aluno_id]
    if not aluno_mentorships:
        return None, "USER_NOT_FOUND"
    return aluno_mentorships, None
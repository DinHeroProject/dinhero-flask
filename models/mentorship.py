class Mentorship:
    def __init__(self, id, mentor_id, aluno_id, start_time, end_time, status, topic, meet_type, notes, aluno_feedback, mentor_feedback):
        self.id = id
        self.mentor_id = mentor_id
        self.aluno_id = aluno_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.topic = topic
        self.meet_type = meet_type
        self.notes = notes
        self.aluno_feedback = aluno_feedback
        self.mentor_feedback = mentor_feedback

    def to_dict(self):
        return {
            "id": self.id,
            "mentor_id": self.mentor_id,
            "aluno_id": self.aluno_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
            "topic": self.topic,
            "meet_type": self.meet_type,
            "notes": self.notes,
            "aluno_feedback": self.aluno_feedback,
            "mentor_feedback": self.mentor_feedback
        }
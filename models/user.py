class User:
    def __init__(self, id, cpf, email, password, first_name, last_name, created_at, updated_at, last_login):
        self.id = id
        self.cpf = cpf
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_login = last_login
        self.first_name = first_name
        self.last_name = last_name

        self.profile = {
            "avatar_url": None,
            "bio": None,
            "date_of_birth": None,
            "gender": None,
            "country": None,
            "language_preference": None,
            "learning_style_preference": None,
            "content_complexity_preference": None,
            "video_length_preference": None
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "cpf": self.cpf,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_login": self.last_login,
            "profile": self.profile
        }


# class Aluno(User):
#     def __init__(self, id, cpf, email, password, first_name, last_name, created_at, updated_at, last_login):
#         super().__init__(id, cpf, email, password, first_name, last_name, created_at, updated_at, last_login)
#         self.financial_info = {
#             "financial_knowledge_level": None,
#             "risk_tolerance": None,
#             "income_level_range": None
#         }

#         self.statistics = {
#             "gamification_points": 0,
#             "total_challenges_completed": 0,
#             "last_active_course_id": None,
#             "last_active_module_id": None
#         }
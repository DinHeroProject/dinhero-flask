class Course:
    def __init__(self, id, title, description, category, created_at, updated_at, author_id, difficulty_level, estimated_duration_minutes, thumbnail_url, is_private, language, number_of_modules, rating, reviews):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.created_at = created_at
        self.updated_at = updated_at
        self.author_id = author_id
        self.difficulty_level = difficulty_level
        self.estimated_duration_minutes = estimated_duration_minutes
        self.thumbnail_url = thumbnail_url
        self.is_private = is_private
        self.language = language
        self.number_of_modules = number_of_modules
        self.rating = rating
        self.reviews = reviews

        self.modules = []
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "author_id": self.author_id,
            "difficulty_level": self.difficulty_level,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "thumbnail_url": self.thumbnail_url,
            "is_private": self.is_private,
            "language": self.language,
            "number_of_modules": self.number_of_modules,
            "rating": self.rating,
            "reviews": self.reviews,
            "modules": [module.to_dict() for module in self.modules]
        }
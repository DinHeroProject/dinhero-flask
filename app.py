from flask import Flask

from routes.user_routes import user_routes
from routes.course_routes import course_routes
from routes.mentorship_routes import mentorship_routes

app = Flask(__name__)

app.register_blueprint(user_routes)
app.register_blueprint(course_routes)
app.register_blueprint(mentorship_routes)

app.run(debug=True)
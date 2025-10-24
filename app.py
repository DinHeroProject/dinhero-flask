from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import os 

load_dotenv()

os.environ['DATABASE_URL'] = os.getenv('DATABASE_URL', 'app/database/dinhero.db')


from app.database.db import init_db
init_db()

from app.routes.user_routes import user_routes
from app.routes.course_routes import course_routes
from app.routes.mentorship_routes import mentorship_routes
from app.routes.auth_routes import auth_routes

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "dfcshvadbnjaksdniu3bf"
app.config["JWT_VERIFY_SUB"]=False


jwt = JWTManager(app)
bcrypt = Bcrypt(app)

app.register_blueprint(user_routes)
app.register_blueprint(course_routes)
app.register_blueprint(mentorship_routes)
app.register_blueprint(auth_routes)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv('PORT', 3333))
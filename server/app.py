
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from extensions import db, bcrypt
# Import models so SQLAlchemy knows about them
from models import User, Note

from resources.auth import auth_bp
from resources.notes import notes_bp

def create_app():
    app = Flask(__name__)

    # Load application configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Initialize JWT authentication
    jwt = JWTManager(app)

    # Initialize database migrations
    migrate = Migrate(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    @app.route("/")
    def home():
        return {
            "message": "Notes API is running",
            "status": "success"
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(port=5555, debug=True)

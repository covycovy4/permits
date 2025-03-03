import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='/home/tsidzo/Desktop/Backendprac/veterinary/templates')
    app.secret_key = os.getenv("SECRET_KEY", "permit123")  # Fallback if not set

    # Database URI from environment variable
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Initialize the extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Importing and registering the blueprint *inside* the create_app function
    from app.routes import main
    app.register_blueprint(main)

    return app


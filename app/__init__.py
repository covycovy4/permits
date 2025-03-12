import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Initialize the Flask app inside the factory function
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
    app.secret_key = os.getenv("SECRET_KEY", "permit123")

    # Fix Heroku's postgres:// issue
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://")

    # Configure the app
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Initialize db and migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app


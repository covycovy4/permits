from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# Drop existing tables




# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='/home/tsidzo/Desktop/Backendprac/veterinary/templates')
    app.secret_key = "permit123"  # Required for using session

    # App config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://permit_user:permit123@localhost:5432/permit_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Initialize the extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Importing and registering the blueprint *inside* the create_app function
    from app.routes import main
    app.register_blueprint(main)

    return app


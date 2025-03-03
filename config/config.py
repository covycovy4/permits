import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    MAIL_SERVER = 'smtp.gmail.com' 
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 
    MAIL_USE_TLS = True 

    # Define database_url first
    database_url = os.getenv("DATABASE_URL", "")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = database_url or "sqlite:///default.db"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


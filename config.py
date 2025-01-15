import os
from dotenv import load_dotenv


# load environment variables from .env file
load_dotenv()

# app config class


class Config:
    """Configuration class for the flask application"""
    SECRET_KEY = os.getenv(
        "SECRET_KEY", "hello")  # used hello as fallback default key
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    SESSION_TYPE = "filesystem"  # for dev purpose
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail server configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

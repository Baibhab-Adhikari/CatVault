import os
import redis


# app config class


class Config:
    """Configuration class for the flask application"""

    SECRET_KEY = os.getenv(
        "SECRET_KEY", "hello")  # used hello as fallback default key

    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    SESSION_TYPE = "redis"  # heroku redis for deployment
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

    uri = os.getenv("DATABASE_URI")
    if uri.startswith("postgres://"):  # type: ignore
        uri = uri.replace("postgres://", "postgresql://", 1)  # type: ignore
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configuration using Redis
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url(
        os.getenv("REDIS_URL"), ssl_cert_reqs=None)  # type: ignore

    # mail server configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

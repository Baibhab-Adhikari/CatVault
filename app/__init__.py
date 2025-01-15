import os

from dotenv import load_dotenv

from cryptography.fernet import Fernet  # type: ignore
from flask import Flask
from flask_bcrypt import Bcrypt  # type: ignore
from flask_mail import Mail  # type: ignore
from flask_migrate import Migrate  # type: ignore
from flask_session import Session  # type: ignore
from flask_sqlalchemy import SQLAlchemy

from config import Config

load_dotenv()

# creating instances of the extensions
bcrypt: Bcrypt = Bcrypt()
db: SQLAlchemy = SQLAlchemy()
session: Session = Session()
mail: Mail = Mail()
migrate: Migrate = Migrate()
# key = "Shr6Eew2IjVx0QHRAWZGxHhn3n9RRwr6Ns_fgyXQuAs="
KEY = os.getenv("ENCRYPTION_KEY")
cipher_suite = Fernet(KEY.encode())


def create_app() -> Flask:
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, template_folder="templates")

    app.config.from_object(Config)  # loading the config file

    # initializing the extensions
    bcrypt.init_app(app)
    db.init_app(app)
    session.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from app.routes import register_routes  # type: ignore
    register_routes(app, db)

    return app

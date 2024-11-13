# initialise the flask app
from flask import Flask
from flask_bcrypt import Bcrypt  # type: ignore
from cs50 import SQL  # type: ignore
from config import Config
from flask_session import Session  # type: ignore 
from cryptography.fernet import Fernet  # type: ignore

# init flask app
app = Flask(__name__)

# load app config
app.config.from_object(Config)

# init flask extensions
bcrypt = Bcrypt(app)
db = SQL("sqlite:///database/catvault.db")
Session(app)
# password encryption advice from copilot for the password manager route
key = app.config["ENCRYPTION_KEY"]
cipher_suite = Fernet(key.encode())

from app import routes

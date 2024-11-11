# Flask best practices advice from chatgpt
import os
from dotenv import load_dotenv


# load environment variables
load_dotenv()

# app config class


class Config:
    """Configuration class for the flask application"""
    SECRET_KEY = os.getenv(
        "SECRET_KEY", "hello")  # used hello as fallback default key
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True  # advice from chatgpt to add security to the session data

# type annotations advice from copilot
from flask import render_template, redirect, session
from typing import Tuple, Union
from app import bcrypt
from functools import wraps
import secrets
import re

# adapted from CS50 Finance


def apology(message: str, code: int = 400) -> Tuple[str, int]:
    """render error message as an apology to the user"""
    return render_template("apology.html", message=message, code=code), code


# adapted from CS50 Finance
def login_required(f):
    """ decoration of routes to enforce login for the user"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def hash_password(password: str) -> str:
    """hashes the password"""
    # referred to flask-bcrypt docs
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_password(password: str, hashed_password: str) -> bool:
    """checks the password"""
    # referred to flask-bcrypt docs
    return bcrypt.check_password_hash(hashed_password, password)


def check_email(email: str) -> bool:
    """checks if the email is valid"""
    # email validation regex from stackoverflow
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None


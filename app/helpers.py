from flask import redirect, session
from typing import Tuple, Union
from app import bcrypt
from functools import wraps
import secrets
import string
import re
from app import cipher_suite


# login required decorator
def login_required(f):
    """ decoration of routes to enforce login for the user"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def hash_password(password: str | None) -> str:
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


def generate_password(length, uppercase, lowercase, numbers, symbols) -> str:
    """generates a random password based on client side input"""
    # password generation
    characters_pool = ""
    # check for user specifications
    if uppercase == 'on':
        characters_pool += string.ascii_uppercase
    if lowercase == 'on':
        characters_pool += string.ascii_lowercase
    if numbers == 'on':
        characters_pool += string.digits
    if symbols == 'on':
        characters_pool += string.punctuation

    # If no checkboxes are checked, provide a default random password of digits
    if not characters_pool:
        characters_pool = string.digits

    return "".join(secrets.choice(characters_pool) for _ in range(int(length)))

# password encryption for the password manager route


def encrypt_password(password: str) -> str:
    """encrypts the password"""
    return cipher_suite.encrypt(password.encode('utf-8')).decode('utf-8')  # type: ignore


def decrypt_password(encrypted_password: str) -> str:
    """decrypts the password"""
    return cipher_suite.decrypt(encrypted_password.encode('utf-8')).decode('utf-8')

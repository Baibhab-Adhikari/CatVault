from sqlalchemy.sql import func

from app import db


class Users(db.Model):  # type: ignore
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(
        db.DateTime, default=func.now(), onupdate=func.now())


class Manager(db.Model):  # type: ignore
    __tablename__ = "manager"
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(200), db.ForeignKey(
        'users.email'), nullable=False)
    website = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(
        db.DateTime, default=func.now(), onupdate=func.now())


class Contact(db.Model):  # type: ignore
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(200), nullable=False)

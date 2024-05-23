from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from cryptography.fernet import Fernet

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(512))
    username = db.Column(db.String(100),unique=True)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    categories = db.relationship('Category', backref='user', lazy=True)
    date_created = db.Column(db.DateTime(timezone=True), default= func.now())
    key = db.Column(db.String(44), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.LargeBinary, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category', backref='posts')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
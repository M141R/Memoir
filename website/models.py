from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    date_created = db.Column(db.DateTime(timezone=True), default= func.now())

class Post(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     text = db.Column(db.Text, nullable=False)
     title = db.Column(db.String(100), nullable=False)
     date_created = db.Column(db.DateTime(timezone=True), default= func.now())
     author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
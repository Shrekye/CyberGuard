from datetime import datetime
from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    red_topics = db.relationship("RedTopic", backref="user", cascade="all, delete-orphan")
    blue_topics = db.relationship("BlueTopic", backref="user", cascade="all, delete-orphan")
    purple_topics = db.relationship("PurpleTopic", backref="user", cascade="all, delete-orphan")


class RedTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BlueTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PurpleTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    topic_id = db.Column(db.Integer)           # id du topic
    topic_type = db.Column(db.String(10))     # "red", "blue", "purple"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(255), nullable=True)

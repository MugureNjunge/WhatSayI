from flask_login import UserMixin
from datetime import datetime

from . import db, login_manager

@login_manager.user_loader
def login_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(120), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author',lazy=True)
    comment = db.relationship('Comments', backref='user', lazy='dynamic')


def __repr__(self):
    return f'User({self.username}, {self.email},{self.image})'

class Post (db.Model):

    id = db.Column(db.Integer, primary_key=True)
    datePosted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    comment =  db.relationship('Comments',backref='post',lazy='dynamic')


def __repr__(self):
    return f"User({self.content},{self.datePosted})"

class Comments (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False) 
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable=False)
    comment = db.Column(db.String(100))


def __repr__(self):
    return f'User({self.comment})'
   

class Quote:
    def __init__(self, author, quote):
        self.author = author
        self.quote = quote
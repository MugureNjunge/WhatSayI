from app import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False ,default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', {self.image_file})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.content}')"

class Quote:
  def __init__(self,author, id, quote):
    self.author = author
    self.id = id
    self.quote = quote     

# class User(UserMixin,db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer,primary_key = True)
#     username = db.Column(db.String(255),index = True)
#     email = db.Column(db.String(255),unique = True,index = True)
#     role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
#     bio = db.Column(db.String(255))
#     profile_pic_path = db.Column(db.String())
#     password_secure = db.Column(db.String(255))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# initialize extentions
app = Flask(__name__)
app.config['SECRET_KEY'] = '4b2ccf690dc0cd9d480745128484079f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from app import routes
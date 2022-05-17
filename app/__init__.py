from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_bootstrap import Bootstrap


from config import config_options


# Initializing extensions:
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
bootstrap = Bootstrap()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message_category='info'

def create_app(config_name):

    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://maureen:Mary01@localhost/blogit'
    db.init_app(app)

    with app.app_context():
        db.create_all()
    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)



    # add views and forms
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # create login view function
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/auth')

    return app
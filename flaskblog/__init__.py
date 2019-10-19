from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Configuration


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

#login_requerd say, where are login router ?
login_manager.login_view = 'users.login' #login route function name // now its not login then redirect login route
login_manager.login_message_category = 'info' # bootstrap class



def create_app(app_config=Configuration):
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from flaskblog.users.route import users_r
    from flaskblog.posts.route import posts
    from flaskblog.main.route import main
    from flaskblog.errors.handler import errors

    app.register_blueprint(users_r)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    return app
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager 
from flask_mail import Mail
from app.config import Config                       # This is the same as before but we migrated all the app.config calls into the config file.
                                                    # This allows us to create a multiple configs for dev, deploy, fallback, production 
# from flask_censor import Censor

db = SQLAlchemy()                                   # This initilizes SQLAlchemy!
mongo = PyMongo()                                   # This initializes PyMongo!
bcrypt = Bcrypt()                                   # This initializes bcrypt!
login_manager = LoginManager()                      # This initializes LoginManager!
login_manager.login_view = 'users.login'            # This is refering to the login() method define in the '/users.login' route!  <--- BLUEPRINT MUST COME BEFORE!!!
login_manager.login_message_category = 'info'       # For those wondering 'info' is a bootstrap class it gives a nice blue-ish hue

mail = Mail()                                       # Now that mail is properly configured we can initialize it!


# By adding the blue prints into this function we can create multiple instances of this app! 

def create_app(config_class=Config):
    app = Flask(__name__)                               # __name__ is referencing the name of this file
    app.config.from_object(Config)                      # We're passing in the Config class we imported, into the app config. 
    
    db.init_app(app)
    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context(): # should handle database migrations
        from .models import database_migrate      
        database_migrate()
    
    from app.users.routes import users                  # Now that we're using Blueprints the import needs to be altered! 
    from app.posts.routes import posts
    from app.main.routes import main
    from app.errors.handlers import errors              # We are importing the instance of the Blueprint, not to confuse this with the name of the folder! 

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    @app.after_request
    def add_header(r):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    return app

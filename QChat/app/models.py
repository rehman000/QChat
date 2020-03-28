from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer              # For email Reset JSON token! 
from flask import current_app                                                       # I need to import this instead of app, because app is now in create_app(), so it's out of scope!
from app import db, login_manager                                                   # Resolves issue with circular imports! Login manager is a flask-extension
from flask_login import UserMixin                                                   # Really useful extension for authentication, and session management, accepts user_id 


@login_manager.user_loader 
def laod_user(user_id):
    return User.query.get(int(user_id))                                             # getter function that helps get the user_id


'''

class Groups(db.Model):
    id = superkey
    name =  string not nullable
    image_file = not nullable
    users = foreign key into the table User
    status = relationship('Post', backref='author', lazy=True) # This has to be many to many relationship! 

'''


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)                                    # Primary Key
    username = db.Column(db.String(20), unique=True, nullable=False)                # Each User will have a username, with a max(20) characters, it must be unique, and Null is not allowed!
    email = db.Column(db.String(120), unique=True, nullable=False)                  # Each User will have an email, with a max(120) characters, it must be unique, and Null is not allowed!
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')    # Each User will have a defualt profile Image, so uniqueness does not apply, since Null is not allowed! 
    password = db.Column(db.String(60), nullable=False)                             # Each User will have passwords, with a max(60) characters, uniqueness does not apply, and Null is not allowed!
    posts = db.relationship('Post', backref='author', lazy=True)                    # This is linked to Posts, Lazy Evaluation is set to: True

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')                        # s.dumps returns a payload! decode 'utf-8' makes sure were returning a string and not bytes 

    @staticmethod                                                                   # This method needs to be static so that it cannot reference self, only the token can be passed in! 
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)                                              # So if everything goes smoothly, and no exceptions go off, return the user in the database with user_id.

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                    # Primary Key
    title = db.Column(db.String(100), nullable=False)                               # Each Post will have a title, with a max(100) characters, uniqueness does not apply, and Null is not allowed!
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)   # Each Post will have a date_posted, with DateTime set to utcnow, current time, and Null is not allowed!
    content = db.Column(db.Text, nullable=False)                                    # Each Post will have a content with no character limit, and Null is not allowed!
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)       # This is using the user id as a ForeignKey, each post must have an Author, so Null is not allowed!


    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20) ])
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired() ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password') ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()                                                     # Get username from the db, if it doesn't exist, i.e database query returns an empty [] we're good! 
        if user:                                                                                                        # If username in fact already exists, i.e database query returns [username], it is not unique! 
            raise ValidationError('This username is already taken. Please choose a different one!')                     # Then we can raise a Validation Error! 

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()                                                           # Get email from the db, if it doesn't exist, i.e database query returns an empty [] we're good! 
        if user:                                                                                                        # If email in fact already exists, i.e database query returns [email], it is not unique! 
            raise ValidationError('This email is already taken. Please choose a different one!')                        # Then we can raise a Validation Error! 



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired() ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20) ])
    email = StringField('Email', validators=[DataRequired(), Email() ])
    picture = FileField('Update Profile Picture', validators=[ FileAllowed(['jpg', 'png']) ])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:                                                                      # Since we're updating the username, we're checking to ensure the new name does not match the old name, because that would raise a false Validation Error!
            user = User.query.filter_by(username=username.data).first()                                                 # Get username from the db, if it doesn't exist, i.e database query returns an empty [] we're good!
            if user:                                                                                                    # If username in fact already exists, i.e database query returns [username], it is not unique! 
                raise ValidationError('This username is already taken. Please choose a different one!')                 # Then we can raise a Validation Error! 

    def validate_email(self, email):
        if email.data != current_user.email:                                                                            # Since we're updating the email, we're checking to ensure the new email does not match the old email, because that would raise a false Validation Error!
            user = User.query.filter_by(email=email.data).first()                                                       # Get username from the db, if it doesn't exist, i.e database query returns an empty [] we're good!
            if user:                                                                                                    # If username in fact already exists, i.e database query returns [username], it is not unique!     
                raise ValidationError('This email is already taken. Please choose a different one!')                    # Then we can raise a Validation Error! 



class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()                                                       # Get username from the db.
        if user is None:                                                                                            # If username does not exist, i.e database query returns [], then raise a validation error!     
            raise ValidationError('There is no account with that email. You must register first.')                  # Then we can raise a Validation Error! 



class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired() ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password') ])

    submit = SubmitField('Reset Password')
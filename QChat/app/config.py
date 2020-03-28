import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')                               # This will not work for you!
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')     # This will not work for you!
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')                # This will not work for you!
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')                # This will not work for you! 
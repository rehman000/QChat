import os


class Config:
    DOMAIN = "qchat.social"
    SQLALCHEMY_TRACK_MODIFICATIONS = False                                  # prevents SQL alchemy FSADeprecationWarning warning
    SEND_FILE_MAX_AGE_DEFAULT = 0                                           # to prevent caching
    FLASK_ENV = os.environ.get('FLASK_ENV')
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
    SECRET_KEY = os.environ.get('SECRET_KEY')                               
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')     
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')                
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')           
    MONGO_URI=os.environ.get('MONGO_URI')
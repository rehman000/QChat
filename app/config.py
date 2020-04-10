import os


class Config:
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
    SECRET_KEY = os.environ.get('SECRET_KEY')                               # Oren This will not work for you!
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')     # Oren This will not work for you!
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')                # Oren This will not work for you! Mine is stored in '.bash_profile'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')                # Oren This will not work for you! Mine is stored in '.bash_profile'
    MONGO_URI=os.environ.get('MONGO_URI')
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    SECRET_KEY = SECRET_KEY = os.environ.get('SECRET_KEY') or '3243452hfgFhs37'
    UPLOAD_FOLDER = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {'png','jpg','jpeg','pdf'}


    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587  
    MAIL_USE_TLS = True

    

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'wiktorgapinski77@gmail.com'

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'wiktorgapinski77@gmail.com'
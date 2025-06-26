import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    DEBUG = True
    SECRET_KEY = SECRET_KEY = os.environ.get('SECRET_KEY') or '3243452hfgFhs37'
    UPLOAD_FOLDER = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {'png','jpg','jpeg','pdf'}
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

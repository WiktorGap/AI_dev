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
    
    # Adres e-mail, z którego będą wysyłane wiadomości (Twój Gmail)
    # PAMIĘTAJ: Zastąp wartości "TWOJ_ADRES" i "TWOJE_HASLO"
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'wiktorgapinski77@gmail.com'
    
    # Hasło do aplikacji wygenerowane w Google (to 16-znakowe hasło)
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'qjuk cpmj muep oeld'
    
    # E-mail admina, na który będziesz otrzymywać wiadomości
    # (zazwyczaj ten sam co MAIL_USERNAME)
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'wiktorgapinski77@gmail.com'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_bootstrap import Bootstrap
from flask_moment import Moment

moment = Moment()
db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    from app.ai_mod import ai_model as ai_bp
    app.register_blueprint(ai_bp)

    return app

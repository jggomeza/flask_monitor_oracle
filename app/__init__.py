from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# Packages
from config import config

# Variables principales
app = Flask(__name__)
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    print(str(__name__) + " -> " + str(config['default'].connection_parameters()))

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # attach routes and custom error pages here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
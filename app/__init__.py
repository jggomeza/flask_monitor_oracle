from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Packages
from config import config

# Variables principales
app = Flask(__name__)
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
cors = CORS(
    app,
    resources={
        r"/*": {"origins": "*"},
        # r"/tablespaces/*": {"origins": "*"},
        # r"/locked/*": {"origins": "*"},
        # r"/inactives/*": {"origins": "*"},
        # r"/collection/*": {"origins": "*"},
        # r"/dolartoday/*": {"origins": "*"},
        # r"/tcseniat/*": {"origins": "*"},
        # r"/telegram/*": {"origins": "*"},
        # r"/ist_banks_status/*": {"origins": "*"},
        # r"/ist_banks_status_yesterday/*": {"origins": "*"},
    }
)


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
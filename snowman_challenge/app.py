"""File containing flask app bootstrap.
"""
from os import environ

from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT

from snowman_challenge.api.v1.views import blueprint
from snowman_challenge.auth import authenticate, identify
from snowman_challenge.database import init_db_session


def create_app(config_filename: str) -> Flask:
    """Creates a flask app.

    :param config_filename: string contains conf filename
    :rtype: Flask
    :return: Flask app object
    """
    flask_app = Flask(__name__, static_folder='templates/static')
    flask_app.register_blueprint(blueprint, url_prefix='/api/v1')
    CORS(flask_app)
    flask_app.config.from_object(config_filename)
    flask_app.config['SECRET_KEY'] = environ.get('JWT_SECRET_KEY', '')
    JWT(flask_app, authenticate, identify)
    init_db_session()
    return flask_app

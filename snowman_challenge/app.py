"""File containing flask app bootstrap.
"""
from flask import Flask
from flask_cors import CORS


from snowman_challenge.database import init_db_session


def create_app(config_filename: str) -> Flask:
    """Creates a flask app.

    :param config_filename: string contains conf filename
    :rtype: Flask
    :return: Flask app object
    """
    app = Flask(__name__, static_folder='templates/static')
    CORS(app)
    app.config.from_object(config_filename)
    init_db_session()
    return app

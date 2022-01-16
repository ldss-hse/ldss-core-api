from pathlib import Path

from dynaconf import FlaskDynaconf
from flask import Flask
from flask_cors import CORS

from core_api.constants import ROOT_PATH
from core_api.extensions.database import init_db


def create_app() -> Flask:
    """Create an application."""
    app = Flask(__name__, static_url_path='', static_folder='../static')

    return app


def configure_app(app: Flask):
    FlaskDynaconf(app, settings_files=["settings.toml", ".secrets.toml"])

    CORS(app)

    init_db(app)


def register_api_blueprints(app):
    from core_api.main.api.v1 import V1_API_BLUEPRINT
    from core_api.main.api.root import V1_ROOT_API_BLUEPRINT

    url_prefix = '/api/v1'

    app.register_blueprint(V1_API_BLUEPRINT, url_prefix=url_prefix)
    app.register_blueprint(V1_ROOT_API_BLUEPRINT, url_prefix='/')

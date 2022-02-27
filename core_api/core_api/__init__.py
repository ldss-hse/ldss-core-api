"""
Module responsible for creation of Flask instance and configuring it
"""
import os
from pathlib import Path

from dynaconf import FlaskDynaconf
from flask import Flask
from flask_cors import CORS

from core_api.extensions.database import init_db
from core_api.extensions.pydantic_spec import PYDANTIC_VALIDATOR

os.environ['PROJECT_ROOT_FOR_DYNACONF'] = str(Path(__file__).parent)
print(f'HEY: PROJECT_ROOT_FOR_DYNACONF: {os.environ["PROJECT_ROOT_FOR_DYNACONF"]}')


def instantiate_app() -> Flask:
    """Create an application."""
    app = Flask(__name__, static_url_path='', static_folder='./static')

    return app


def configure_app(app: Flask):
    """
    configuring Flask application
    :param app: Flask instance
    """
    print(f'Flask config before loading settings: {app.config}')
    print(f'Flask config before loading settings: {dir(app.config)}')
    FlaskDynaconf(app, settings_files=["settings.toml", ".secrets.toml"])
    print(f'Flask config after loading settings: {app.config}')
    print(f'Flask config before loading settings: {dir(app.config)}')

    CORS(app)

    PYDANTIC_VALIDATOR.register(app)

    init_db(app)


def register_api_blueprints(app):
    """registering all Flask application blueprints"""

    # pylint: disable=import-outside-toplevel
    from core_api.main.api.v1 import V1_API_BLUEPRINT
    from core_api.main.api.root import V1_ROOT_API_BLUEPRINT

    url_prefix = '/api/v1'

    app.register_blueprint(V1_API_BLUEPRINT, url_prefix=url_prefix)
    app.register_blueprint(V1_ROOT_API_BLUEPRINT, url_prefix='/')


def create_app():
    print('Creating app!!!!')
    print(f'Current directory: {Path(__file__)}')
    app = instantiate_app()
    configure_app(app)
    register_api_blueprints(app)

    return app

from pathlib import Path

from dynaconf import FlaskDynaconf
from flask import Flask

from core_api.constants import ROOT_PATH
from core_api.extensions_factory.database import init_db


def create_app() -> Flask:
    """Create an application."""
    app = Flask(__name__, static_url_path='', static_folder='../static')

    from core_api.main.api.v1 import V1_API_BLUEPRINT
    from core_api.main.api.root import V1_ROOT_API_BLUEPRINT

    url_prefix = '/api/v1'

    app.register_blueprint(V1_API_BLUEPRINT, url_prefix=url_prefix)
    app.register_blueprint(V1_ROOT_API_BLUEPRINT, url_prefix='/')

    return app


def configure_app(app: Flask):
    FlaskDynaconf(app, settings_files=["settings.toml", ".secrets.toml"])

    # db_dir = ROOT_PATH / app.config.DATABASE_DIR
    # db_dir = Path('.') / app.config.DATABASE_DIR
    # db_dir.mkdir(parents=True, mode=777, exist_ok=True)

    # app.config.SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_dir}'
    # app.config.SQLALCHEMY_DATABASE_URI = f'sqlite:///db/main.db'
    # app.config.SQLALCHEMY_DATABASE_URI = f'sqlite:////Users/demidovs/db/main.db'
    # app.config.SQLALCHEMY_DATABASE_URI = f'sqlite:///'+ '/Users/demidovs/Documents/projects/1_hse/ldss-core-api/db/main.db'

    init_db(app)

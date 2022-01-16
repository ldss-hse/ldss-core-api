from dynaconf import FlaskDynaconf
from flask import Flask


def create_app() -> Flask:
    """Create an application."""
    app = Flask(__name__, static_url_path='', static_folder='../static')

    from core_api.main.api.v1 import V1_API_BLUEPRINT
    from core_api.main.api.root import V1_ROOT_API_BLUEPRINT

    url_prefix = '/api/v1'

    app.register_blueprint(V1_API_BLUEPRINT, url_prefix=url_prefix)
    app.register_blueprint(V1_ROOT_API_BLUEPRINT, url_prefix='/')

    FlaskDynaconf(app, settings_files=["settings.toml", ".secrets.toml"])

    return app

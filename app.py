from core_api import create_app, configure_app, register_api_blueprints

APP = create_app()

configure_app(APP)
register_api_blueprints(APP)

if __name__ == "__main__":
    APP.run(debug=True)

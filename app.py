from core_api import create_app, configure_app

APP = create_app()

configure_app(APP)


if __name__ == "__main__":
    APP.run(debug=True)

"""Root module for the Flask application"""

from core_api import create_app

if __name__ == "__main__":
    create_app().run(host='0.0.0.0', debug=False, use_debugger=False, use_reloader=False)

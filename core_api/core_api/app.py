"""Root module for the Flask application"""

from core_api import create_app

if __name__ == "__main__":
    create_app().run(debug=True)

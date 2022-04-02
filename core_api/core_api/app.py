"""Root module for the Flask application"""
import os

from core_api import create_app

if __name__ == "__main__":
    app_port = os.environ.get('PORT', 5000)
    print(f'Running application on port: {app_port}')
    create_app().run(host='0.0.0.0', port=app_port,
                     debug=False, use_debugger=False, use_reloader=False)

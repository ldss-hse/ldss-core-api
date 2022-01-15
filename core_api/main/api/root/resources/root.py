from flask import send_from_directory
from flask_restful import Resource

from core_api.constants import TEMPLATES_PATH


class RestAPIRoot(Resource):
    def get(self):
        return send_from_directory(TEMPLATES_PATH, 'index.html')

"""
A module for handling static files
"""

from flask import send_from_directory

from core_api.constants import TEMPLATES_PATH
from core_api.main.api.root import V1_ROOT_API_BLUEPRINT


@V1_ROOT_API_BLUEPRINT.route('/', methods=['GET'])
def get():
    """
    Serving pre-built client application
    :return: HTML file
    """
    return send_from_directory(TEMPLATES_PATH, 'index.html')

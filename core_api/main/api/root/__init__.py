from flask import Blueprint
from flask_restful import Api

V1_ROOT_API_BLUEPRINT = Blueprint('root_api', __name__)

root_api = Api(V1_ROOT_API_BLUEPRINT)

# pylint: disable=wrong-import-position
from .resources.root import RestAPIRoot

root_api.add_resource(RestAPIRoot, '/')

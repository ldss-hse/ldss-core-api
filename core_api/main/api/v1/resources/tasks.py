import json

from flask import request, jsonify, Response
from flask_restful import Resource

from core_api.main.models.tasks import TasksModel
from core_api.extensions.database import get_database_session_for_flask


class RestAPITasks(Resource):
    def get(self):
        return {'this is': 'tasks get'}

    def post(self):
        json_data = request.get_json()
        u = TasksModel(name=json_data['taskName'])
        get_database_session_for_flask().add(u)
        get_database_session_for_flask().commit()

        response = {
            'taskID': u.id
        }
        return Response(json.dumps(response),
                        status=200,
                        mimetype='application/json')

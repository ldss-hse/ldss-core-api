from flask_restful import Resource


class RestAPITasks(Resource):
    def get(self):
        return {'this is': 'tasks get'}

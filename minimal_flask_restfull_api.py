from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
args = parser.parse_args()

todos = {}

resource_fields  = {
    'tasks': fields.String,
    'url': fields.Url('todo_ep')
}


class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task
        self.status = 'active'


class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        return TodoDao(todo_id='my_todo', task='Remember the milk')


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class TodosSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}, 200, {'Etag': 'Created Successfully'}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}, 201, {'Etag': 'some-string'}


api.add_resource(HelloWorld, '/', endpoint='todo_ep')
api.add_resource(TodosSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)

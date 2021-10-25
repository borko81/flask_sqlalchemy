from config import app, jwt
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from config.models import UserModel

parser = reqparse.RequestParser()
parser.add_argument('name', help='username can not be blank', required=True)
parser.add_argument('password', help='password can not be blank', required=True)


class UserResourse(Resource):
    def get(self):
        """
        hint:
            curl 127.0.0.1:5000/users -X GET
        :return: json data with name of users
        """
        users = UserModel.query.all()
        data = {'users': [u.to_json() for u in users]}
        return data

    def post(self):
        """
        hint:
            curl 127.0.0.1:5000/users -X POST -d "name=borko" -d "password=borko"
        :return: json message
        """
        data = parser.parse_args()
        name = data['name']
        password = data['password']
        if not UserModel.find_by_name(name):
            u = UserModel(name=name, password=password)
            u.hashed_password(password)
            u.save()
            return {'message': 'User was created successfully'}, 201
        return {'message': 'Not allowed this name'}, 400


class UserJWT(Resource):
    def post(self):
        data = parser.parse_args()
        name = data['name']
        password = data['password']
        if name and password:
            current_user = UserModel.find_by_name(name)
            if current_user and current_user.check_password(password):
                access_token = create_access_token(identity=current_user.id)
                return {'token': access_token}, 201
            return {'message': 'Error with generate jwt'}, 400

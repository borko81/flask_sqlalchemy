from flask import request

from config.models import CarModel

from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse

"""
class CarModel(ModuleHelper):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    card = db.Column(db.String(250), unique=True)
    tax_id = db.Column(db.Integer, db.ForeignKey('tax.id'))

    def to_json(self):
        return {'name': self.name, 'card': self.card, 'tax_id': self.tax_id}
"""


class CarsResourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', help='username can not be blank', required=True)
    parser.add_argument('card', help='card can not be blank', required=True)
    parser.add_argument('tax_id', help='tax_id can not be blank', required=True)

    def get(self):
        """
        hint:
            curl 127.0.0.1:5000/cars
            curl 127.0.0.1:5000/cars?order_by=1
        :return: json with all cars data
        """
        order_by = request.args.get('order_by', type=int)
        if not order_by:
            cars = CarModel.query.all()
            data = {'cars': [c.to_json() for c in cars]}
            return data, 200
        cars = CarModel.query.filter_by(tax_id=order_by)
        data = {'cars': [c.to_json() for c in cars]}
        return data, 200

    def post(self):
        """
        hint:
            curl 127.0.0.1:5000/cars -X POST -d "name=borko" -d "card=1111" -d "tax_id=2"
        :return: json with message for success and data for new created car
        """
        args = self.parser.parse_args()
        name = args['name']
        card = args['card']
        tax_id = args['tax_id']
        new_car = CarModel(name=name, card=card, tax_id=tax_id)
        new_car.save_to_db()
        return {'message': 'Successfully create new car', 'car': new_car.to_json()}, 201


class CarResourse(Resource):

    def get(self, _id):
        car = CarModel.find_by_id(_id)
        if not car:
            return {"message": f"Error not found car this id: {_id}"}, 400
        return car.to_json(), 200

    def put(self, _id):
        """
        hint:
            curl 127.0.0.1:5000/car/4 -X PUT
        :param _id: int
        :return: error message, when not found car with this id, i way to success return json with data
        """
        car = CarModel.find_by_id(_id)
        if not car:
            return {"message": f"Error not found car this id: {_id}"}, 400
        parser = reqparse.RequestParser()
        parser.add_argument('name', help='username can not be blank', required=False)
        parser.add_argument('card', help='card can not be blank', required=False)
        parser.add_argument('tax_id', help='tax_id can not be blank', required=False)
        args = parser.parse_args()
        car.name = args['name'] or car.name
        car.card = args['card'] or car.card
        car.tax_id = args['tax_id'] or car.tax_id
        car.save_to_db()
        car = CarModel.find_by_id(_id)
        return car.to_json(), 200

    @staticmethod
    def delete(_id):
        """
        hint:
            curl 127.0.0.1:5000/car/4 -X DELETE
        :param _id: int
        :return: Error message when not found car with this id, otherwise delete car
        """
        car = CarModel.find_by_id(_id)
        if not car:
            return {"message": f"Error not found car this id: {_id}"}, 400
        car.delete_from_db()
        return {'message': f'Successfully delete car with id: {_id}'}, 204

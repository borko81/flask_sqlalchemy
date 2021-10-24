from flask import jsonify

from config import api
from config.models import TaxModel
from flask_restful import Resource, reqparse


class AllTaxResurse(Resource):
    """
        Return all taxes from database
    """
    parser = reqparse.RequestParser()
    parser.add_argument('name', help='Name is required')
    parser.add_argument('price', help='Price is required')
    parser.add_argument('id', type=int, help='Price', required=False)

    def get(self):
        """
        hint:
            curl 127.0.0.1:5000/tax
        :return: Json with data
        """
        all_tax = TaxModel.query.all()
        data = {'tax': []}
        for tax in all_tax:
            data['tax'].append({'id': tax.id, 'name': tax.name, 'price': tax.price,
                                'car_in_this_tax': [t.to_json() for t in tax.cars]})
        return data, 200

    def post(self):
        """
        hint:
            curl 127.0.0.1:5000/tax -P POST -d "name=tax_three" -d "price=3"
        :return: Json message and status code 201 for create
        """
        args = self.parser.parse_args()
        name = args['name']
        price = args['price']
        if args and price:
            TaxModel(name=name, price=price).save_to_db()
            return {'message': 'New Tax was created successfully'}, 201
        return {'message': 'Error invalid param'}, 400

    def delete(self):
        args = self.parser.parse_args()
        """
            By type of args, use two different methods to delete from database
            If id in data, search in data, if name in data, search tax with name,
            if id and name in data, search by first parameter.
            If not add correct data return error message
            hint: 
                curl 127.0.0.1:5000/tax -X DELETE -d "id=3"
                curl 127.0.0.1:5000/tax -X DELETE -d "name=tax_four"
        """
        if args['id']:
            _id = args['id']
            t = TaxModel.find_by_id(_id)
            if t:
                t.delete_from_db()
                return {'message': 'Successfully delete tax by id'}, 204
            else:
                return {'message': 'Gain error'}, 400
        elif args['name']:
            t = TaxModel.find_by_name(args['name'])
            if t:
                t.delete_from_db()
                return {'message': 'Successfully delete tax by name'}, 204
            return {'message': 'Gain error'}, 400
        return {'message': 'Gain error'}, 400


class TaxResurse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', help='Name is required')
    parser.add_argument('price', help='Price is required')
    """
        Return current tax
        hint:
            curl 127.0.0.1:5000/tax/1
    """
    def get(self, _id):
        tax = TaxModel.find_by_id(_id)
        if not tax:
            return {'message': 'Cannot find id'}, 400
        data = {'tax': {'id': tax.id, 'name': tax.name, 'price': tax.price,
                        'car_in_this_tax': [t.to_json() for t in tax.cars]}}
        return data, 200

    def put(self, _id):
        """
        hint:
            curl 127.0.0.1:5000/tax/3 -X PUT -d "price=15" -d "name=FOUR"
        :param _id: int
        :return: Json with message
        """
        tax = TaxModel.find_by_id(_id)
        args = self.parser.parse_args()

        if not tax:
            return {'message': 'Not found tax with this id'}, 400

        tax.name = args['name'] or tax.name
        tax.price = args['price'] or tax.price
        tax.save_to_db()
        return {'message': 'Successfully change elements of tax'}, 200

    @staticmethod
    def delete(_id):
        """
        hint:
            curl 127.0.0.1:5000/tax/3 -X DELETE
        :param _id: int
        :return: Json with data
        """
        tax = TaxModel.find_by_id(_id)
        if not tax:
            return {'message': 'Not found tax with this id'}, 401
        tax.delete_from_db()
        return {'message': 'This tax was deleted successfully'}, 204

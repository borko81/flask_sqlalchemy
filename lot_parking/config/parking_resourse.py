from flask import jsonify, request
from datetime import datetime
from config import api
from config.models import TaxModel, UserModel, CarModel, ParkingModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required


class ParkingResourse(Resource):
    def get(self):
        parking = ParkingModel.query.all()
        return {'cars': [p.to_json() for p in parking]}

    def post(self):
        """
        hint:
            curl 127.0.0.1:5000/parking?card='1111' -X POST
        :return:
        """
        _card = request.args.get('card')
        car = CarModel.query.filter_by(card=_card).first()
        lot_car = ParkingModel.query.filter_by(car_id=car.id).order_by(ParkingModel.id.desc()).first()
        if not lot_car.out_lot:
            tax = TaxModel.find_by_id(car.tax_id)
            lot_car.out_lot = datetime.now()
            lot_car.save_to_db()
            duration = int((lot_car.out_lot - lot_car.in_lot).total_seconds() / 3600)  # Convert to hour's
            price = duration * tax.price
            return {'message': car.id, 'tax': tax.price, 'out': str(duration), 'price': price}
        ParkingModel(car_id=car.id).save_to_db()
        return {'message': "New car added to lot"}

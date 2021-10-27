import json
import unittest
from config import db
from run import app

from config.models import ParkingModel, CarModel, TaxModel


class TestParkingResourse(unittest.TestCase):

    URL = 'http://127.0.0.1:5000/parking'

    def setUp(self) -> None:
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
        self.client = app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        db.drop_all()


    def test_get_all_cars_from_parking(self):
        TaxModel(name='primary', price=1).save_to_db()
        CarModel(name='Car One', card='111', tax_id=1).save_to_db()
        ParkingModel(car_id=1).save_to_db()
        ParkingModel.query.all()
        response = self.client.get(self.URL)
        cars_result = json.loads(response.get_data())['cars']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cars_result[0]['name'], "Car One")
        print(f"[+] test {self.test_get_all_cars_from_parking.__name__}: finish")




if __name__ == '__main__':
    unittest.main()
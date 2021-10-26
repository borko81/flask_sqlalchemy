import json
import unittest
from config import db
from run import app
from config.models import CarModel, TaxModel


class TestCars(unittest.TestCase):
    URL = "http://127.0.0.1:5000/cars"

    def setUp(self) -> None:
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
        self.client = app.test_client()
        db.create_all()

    def test_get_cars(self):
        response = self.client.get(self.URL)
        self.assertEqual(200, response.status_code)
        response = self.client.get("http://127.0.0.1:5000/cars?order_by=1")
        self.assertEqual(200, response.status_code)

    def test_post_new_car(self):
        TaxModel(name='test', price=3).save_to_db()
        response = self.client.post(
            self.URL,
            data={"name": "test", "card": "1234", "tax_id": 1}
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual("Successfully create new car", json.loads(response.get_data())['message'])
        self.assertEqual({'name': 'test', 'card': '1234', 'tax_id': 1, 'tax_name': 'test'}, json.loads(response.get_data())['car'])

    def tearDown(self) -> None:
        db.drop_all()


if __name__ == '__main__':
    unittest.main()

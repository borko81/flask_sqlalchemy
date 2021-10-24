import json
import unittest
from config import db
from run import app

from config.models import TaxModel


class TestTaxesOne(unittest.TestCase):
    URL = 'http://127.0.0.1:5000/tax/1'

    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
        self.client = app.test_client()
        db.create_all()

    def test_successfully_return_tax_one(self):
        TaxModel(name='Test', price=1).save_to_db()
        response = self.client.get(self.URL)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(TaxModel.query.all()))
        print('[+]', TestTaxesOne.test_successfully_return_tax_one.__name__)

    def test_put_return_error_message_when_not_found_id(self):
        test_data = {"name": "TEST", "price": 10}
        response = self.client.put(
            self.URL, data=json.dumps(test_data)
        )
        self.assertEqual(401, response.status_code)
        print('[+]', TestTaxesOne.test_put_return_error_message_when_not_found_id.__name__)

    def test_put_change_data_when_id_in_databse(self):
        TaxModel(name='Test', price=1).save_to_db()
        test_data = {"name": "TEST", "price": 10}
        response = self.client.put(
            self.URL, data=json.dumps(test_data)
        )
        self.assertEqual(200, response.status_code)
        print('[+]', TestTaxesOne.test_put_change_data_when_id_in_databse.__name__)


    def tearDown(self) -> None:
        db.drop_all()


if __name__ == '__main__':
    unittest.main()

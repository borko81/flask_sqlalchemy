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
        self.assertEqual(400, response.status_code)
        print('[+]', TestTaxesOne.test_put_return_error_message_when_not_found_id.__name__)

    def test_put_change_data_when_id_in_databse(self):
        TaxModel(name='Test', price=1).save_to_db()
        test_data = {"name": "TEST"}
        response = self.client.put(
            self.URL, data=test_data
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(TaxModel.find_by_id(1).name, 'TEST')
        self.assertEqual(TaxModel.find_by_id(1).price, 1)
        print('[+]', TestTaxesOne.test_put_change_data_when_id_in_databse.__name__)

    def test_delete_when_id_not_correct(self):
        response = self.client.delete(
            self.URL
        )
        self.assertEqual(401, response.status_code)
        print('[+]', TestTaxesOne.test_delete_when_id_not_correct.__name__)

    def test_delete_when_id_is_correct(self):
        TaxModel(name='Test', price=1).save_to_db()
        response = self.client.delete(
            self.URL
        )
        self.assertEqual(204, response.status_code)
        print('[+]', TestTaxesOne.test_delete_when_id_is_correct.__name__)

    def tearDown(self) -> None:
        db.drop_all()


class TestAllTax(unittest.TestCase):
    URL = 'http://127.0.0.1:5000/tax'

    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
        self.client = app.test_client()
        db.create_all()

    def test_post_request(self):
        response = self.client.post(
            self.URL, data={'name': 'test', 'price': 1}
        )
        self.assertEqual(201, response.status_code)
        t = TaxModel.find_by_id(1)
        self.assertEqual(t.name == 'test', t.price == 1)
        print('[+]', TestAllTax.test_post_request.__name__)

    def test_post_with_invalid_argument(self):
        response = self.client.post(
            self.URL, data={'name': 'test'}
        )
        self.assertEqual(400, response.status_code)
        print('[+]', TestAllTax.test_post_with_invalid_argument.__name__)

    def test_get_all_tax(self):
        response = self.client.get(
            self.URL
        )
        self.assertEqual(200, response.status_code)
        print('[+]', TestAllTax.test_get_all_tax.__name__)

    def test_delete_when_id_not_found(self):
        response = self.client.delete(
            self.URL, data={'id': 1}
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual('Gain error', json.loads(response.get_data(as_text=True))['message'])
        print('[+]', TestAllTax.test_delete_when_id_not_found.__name__)

    def test_delete_when_id_found(self):
        TaxModel(name='test', price=1).save_to_db()
        response = self.client.delete(
            self.URL, data={'id': 1}
        )
        self.assertEqual(204, response.status_code)
        print('[+]', TestAllTax.test_delete_when_id_found.__name__)

    def test_delete_when_name_found(self):
        TaxModel(name='test', price=1).save_to_db()
        response = self.client.delete(
            self.URL, data={'name': 'test'}
        )
        self.assertEqual(204, response.status_code)
        print('[+]', TestAllTax.test_delete_when_name_found.__name__)

    def test_delete_when_name_not_found(self):
        TaxModel(name='test', price=1).save_to_db()
        response = self.client.delete(
            self.URL, data={'name': 'test123'}
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual('Gain error', json.loads(response.get_data(as_text=True))['message'])
        print('[+]', TestAllTax.test_delete_when_name_not_found.__name__)

    def test_delete_when_has_bad_parameters(self):
        TaxModel(name='test', price=1).save_to_db()
        response = self.client.delete(
            self.URL
        )
        self.assertEqual(400, response.status_code)
        print('[+]', TestAllTax.test_delete_when_has_bad_parameters.__name__)

    def tearDown(self) -> None:
        db.drop_all()


if __name__ == '__main__':
    unittest.main()

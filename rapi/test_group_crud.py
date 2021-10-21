import unittest

from config import app, db
import requests


class TestGroup(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # self.client = app.test_client()
        db.create_all()

    def test_get_method(self):
        response = requests.get('127.0.0.1:5000/groups')
        print(response)
        self.assertEqual(response.status_code, 200)

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()


if __name__ == '__main__':
    unittest.main()

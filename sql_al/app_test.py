import json
import unittest
import app


class BaseTest(unittest.TestCase):
    app.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///checking.db"
    app.app.config['TESTING'] = True

    def setUp(self):
        app.db.create_all()
        self.app = app.app.test_client()
        self.app.testing = True
        self.url = 'http://127.0.0.1:5000/'

    def test_get_all(self):
        u = app.User(username='test', email='test@abv.bg')
        app.db.session.add(u)
        app.db.session.commit()
        response = self.app.get(self.url + 'user')
        data = json.loads(response.get_data())
        self.assertEqual(data[0]['username'], 'test')
        self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        app.db.session.remove()
        app.db.drop_all()



if __name__ == '__main__':
    unittest.main()

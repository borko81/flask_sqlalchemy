import json
import unittest
from config import db
from run import app

from config.models import UserModel


class TestUser(unittest.TestCase):
    URL = "http://127.0.0.1:5000/users"

    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
        self.client = app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        db.drop_all()

    def test_show_users(self):
        UserModel(name='Test', password='abc123').save_to_db()
        response = self.client.get(self.URL)
        self.assertEqual(200, response.status_code)
        print(f"[+] Test {self.test_show_users.__name__} complete successfully.")

    def test_post_user_when_all_is_ok(self):
        response = self.client.post(
            self.URL,
            data={"name": "Test", "password": "123abc"}
        )
        self.assertEqual(201, response.status_code)
        u = UserModel.find_by_id(1)
        self.assertEqual("Test", u.name)
        print(f"[+] Test {self.test_post_user_when_all_is_ok.__name__} complete successfully.")

    def test_post_user_when_password_not_has_four_character(self):
        response = self.client.post(
            self.URL,
            data={"name": "Test", "password": "abv"}
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual("Password there must be at least one number", json.loads(response.get_data())['message'])
        print(f"[+] Test {self.test_post_user_when_password_not_has_four_character.__name__} complete successfully.")

    def test_post_user_when_password_not_have_at_least_one_digit(self):
        response = self.client.post(
            self.URL,
            data={"name": "Test", "password": "abvc"}
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual("Password there must be at least one number", json.loads(response.get_data())['message'])
        print(
            f"[+] Test {self.test_post_user_when_password_not_have_at_least_one_digit.__name__} complete successfully.")


if __name__ == '__main__':
    unittest.main()

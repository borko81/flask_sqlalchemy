import unittest
from minimal_work_example import app
from copy import deepcopy
import json
import minimal_work_example

total_item = len(minimal_work_example.TODOS)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.backup_items = deepcopy(minimal_work_example.TODOS)
        self.app = app.test_client()
        self.app.testing = True
        self.data = json.loads(self.app.get('/todos').get_data())

    def tearDown(self):
        minimal_work_example.TODOS = self.backup_items


class Testing(BaseTest):

    def test_show_all_todos(self):
        response = self.app.get('/todos')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), total_item)
        print("Finish with testing show_all_todos")

    def test_show_specific_item_from_data(self):
        response = self.app.get('/todos/todo1')
        data = json.loads(response.get_data())
        self.assertEqual(data['task'], 'build an API')
        self.assertEqual(response.status_code, 200)
        print("Finish with success show specific item")

    def test_raise_error_when_try_to_get_element_who_is_not_in_list(self):
        response = self.app.get('/todos/todo11')
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        item = 'For testing'
        response = self.app.post('/todos', data={'task': item})
        data = json.loads(self.app.get('/todos').get_data())
        self.assertEqual(len(data), total_item + 1)

    def test_new_item_from_todos(self):
        response = self.app.put('/todos/checking', data={'task': 'Put item'})
        self.assertEqual(minimal_work_example.TODOS['checking']['task'], 'Put item')
        data = json.loads(self.app.get('/todos').get_data())
        self.assertEqual(len(data), total_item + 1)

    def test_update_item_when_given_name_in_todos(self):
        response = self.app.put('/todos/todo1', data={'task': 'Item now is changed'})
        self.assertEqual(response.status_code, 201)

    def test_delete_when_item_is_ok_should_decrease_all_items(self):
        response = self.app.delete('/todos/todo1')
        data = json.loads(self.app.get('/todos').get_data())
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(data), total_item - 1)

    def test_delete_when_item_not_in_data_should_raise_error(self):
        response = self.app.delete('/todos/todo11')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()

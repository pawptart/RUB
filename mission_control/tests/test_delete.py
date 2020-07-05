import json
import os
import unittest
from mission_control import app


class TestDelete(unittest.TestCase):

    os.environ['ENVIRONMENT'] = 'test'
    CONFIG_PATH = os.path.abspath('../config_test.json')

    def setUp(self):
        self.app = app.test_client()
        if os.path.exists(self.CONFIG_PATH):
            os.remove(self.CONFIG_PATH)

    def tearDown(self):
        if os.path.exists(self.CONFIG_PATH):
            os.remove(self.CONFIG_PATH)

    def test_delete_with_existing_config(self):
        # Should redirect to index and write a blank config file
        with open(self.CONFIG_PATH, 'w') as file:
            json.dump({'test': 'test'}, file)

        response = self.app.get('/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bot configuration was deleted successfully.', response.data)
        self.assertTrue(os.path.isfile(self.CONFIG_PATH))

        with open(self.CONFIG_PATH, 'r') as file:
            config_data = json.load(file)

        self.assertEqual(config_data, {})

    def test_delete_without_config(self):
        # Should handle non-existent config gracefully
        response = self.app.get('/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bot configuration does not exist.', response.data)
        self.assertTrue(os.path.isfile(self.CONFIG_PATH))

        with open(self.CONFIG_PATH, 'r') as file:
            config_data = json.load(file)

        self.assertEqual(config_data, {})

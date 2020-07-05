import json
import os
import unittest
from mission_control import app


class TestIndex(unittest.TestCase):

    os.environ['ENVIRONMENT'] = 'test'
    CONFIG_PATH = os.path.abspath('../config_test.json')

    def setUp(self):
        self.app = app.test_client()
        if os.path.exists(self.CONFIG_PATH):
            os.remove(self.CONFIG_PATH)

    def tearDown(self):
        if os.path.exists(self.CONFIG_PATH):
            os.remove(self.CONFIG_PATH)

    def test_get_index(self):
        # Should always result in 200 and display a new button
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create a New Bot', response.data)

    def test_get_index_with_existing_config(self):
        # Should always result in 200, but display delete instead of new
        with open(self.CONFIG_PATH, 'w') as file:
            json.dump({'test': 'test'}, file)

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Delete Existing Bot', response.data)

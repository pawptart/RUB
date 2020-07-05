import json
import os
import unittest
from mission_control import app


class TestEdit(unittest.TestCase):

    os.environ['ENVIRONMENT'] = 'test'
    CONFIG_PATH = os.path.abspath('../config_test.json')

    def setUp(self):
        self.app = app.test_client()
        if os.path.exists(self.CONFIG_PATH):
            os.remove(self.CONFIG_PATH)

    def tearDown(self):
        if os.path.exists(self.CONFIG_PATH):
            os.remove(self.CONFIG_PATH)

    def test_get_edit_without_existing_config(self):
        # Should redirect to index and disallow editing
        response = self.app.get('/edit', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No existing configuration found', response.data)

    def test_get_index_with_existing_config(self):
        # Should render the edit form
        valid_config = {
            "reddit": {
                "username": "TestBot"
            },
            "handler": "economy"
        }
        with open(self.CONFIG_PATH, 'w') as file:
            json.dump(valid_config, file)

        response = self.app.get('/edit', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Editing Bot', response.data)

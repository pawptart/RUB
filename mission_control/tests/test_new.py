import json
import os
import unittest
from mission_control import app


class TestNew(unittest.TestCase):

    os.environ['ENVIRONMENT'] = 'test'
    CONFIG_PATH = os.path.abspath('../config_test.json')

    def setUp(self):
        self.app = app.test_client()
        if os.path.exists(self.CONFIG_PATH):
            os.remove(self.CONFIG_PATH)

    def tearDown(self):
        if os.path.exists(self.CONFIG_PATH):
            os.remove(self.CONFIG_PATH)

    def test_get_new(self):
        # Should render the new form if no config is present
        response = self.app.get('/new', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_new_with_existing_config(self):
        # Should redirect to index and prevent override of old config
        with open(self.CONFIG_PATH, 'w') as file:
            json.dump({'test': 'test'}, file)

        response = self.app.get('/new', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

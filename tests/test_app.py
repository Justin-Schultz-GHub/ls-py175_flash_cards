import unittest
import os
import shutil
from app import app, get_data_dir, get_deck_path

class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.data_path = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_path, exist_ok=True)

    def test_create_deck(self):
        pass

    def test_create_nameless_deck(self):
        pass

    def test_create_existing_deck(self):
        pass

    def test_rename_deck(self):
        pass



    def tearDown(self):
        shutil.rmtree(self.data_path, ignore_errors=True)
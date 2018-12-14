import os
import unittest

from clean_airtomation.config import Config

current_directory = os.path.dirname(__file__)


class ConfigTest(unittest.TestCase):
    def test_config(self):
        config = Config()
        conf = config.read_config(base_dir=current_directory)
        self.assertEqual(conf['apikey'], 'API_KEY')
        self.assertEqual(conf['installationId'], 123)

import unittest

from CleanAirtomation.Config import Config


class ConfigTest(unittest.TestCase):
    def test(self):
        config = Config()
        conf = config.read_config()
        self.assertEqual(conf['apikey'], 'API_KEY')
        self.assertEqual(conf['installationId'], 123)

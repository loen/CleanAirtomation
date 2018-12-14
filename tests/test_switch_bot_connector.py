import unittest
from unittest import mock

from clean_airtomation.switch_bot_connector import SwitchBotConnector


class SwitchBotConnectorTest(unittest.TestCase):

    def mocked_call_true(*popenargs, **kwargs):
        return 0

    def mocked_call_false(*popenargs, **kwargs):
        return 1

    @mock.patch('subprocess.call', mocked_call_true)
    def test_push_the_button_success(self):
        conn = SwitchBotConnector('sample_command', 'FF:AA:12:A2:55:66')
        self.assertTrue(conn.push_the_button())

    @mock.patch('subprocess.call', mocked_call_false)
    def test_push_the_button_failure(self):
        conn = SwitchBotConnector('sample_command', 'FF:AA:12:A2:55:66')
        self.assertFalse(conn.push_the_button())

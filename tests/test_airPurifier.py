import unittest
from unittest import mock

from CleanAirtomation.AirPurifier import AirPurifier


class MockedConfig:

    def read_config(self):
        return {'commandPath': 'some_command',
                'onButtonMac': 'AD:1W:87:PO:12:11',
                'offButtonMac': 'FF:FF:FF:FF:FF:FF'}


class AirPurifierTest(unittest.TestCase):

    def cmd_call_true(*popenargs, **kwargs):
        return 0

    def cmd_call_false(*popenargs, **kwargs):
        return 1

    def cmd_call_false_for_off_button(*popenargs, **kwargs):
        if popenargs[0][3] == 'FF:FF:FF:FF:FF:FF':
            return 1
        else:
            return 0

    def cmd_call_false_for_on_button(*popenargs, **kwargs):
        if popenargs[0][3] == 'AD:1W:87:PO:12:11':
            return 1
        else:
            return 0

    @mock.patch('subprocess.call', cmd_call_true)
    def test_switch_on_success(self):
        air_purifier = AirPurifier(MockedConfig())
        self.assertTrue(air_purifier.turn_on())
        self.assertEqual(1, air_purifier.get_state())

    @mock.patch('subprocess.call', cmd_call_false)
    def test_switch_on_failure(self):
        air_purifier = AirPurifier(MockedConfig())
        self.assertFalse(air_purifier.turn_on())
        self.assertEqual(0, air_purifier.get_state())

    @mock.patch('subprocess.call', cmd_call_true)
    def test_switch_off_success(self):
        air_purifier = AirPurifier(MockedConfig())
        self.assertTrue(air_purifier.turn_off())
        self.assertEqual(0, air_purifier.get_state())

    @mock.patch('subprocess.call', cmd_call_false)
    def test_switch_off_failure(self):
        air_purifier = AirPurifier(MockedConfig())
        self.assertFalse(air_purifier.turn_off())
        self.assertEqual(0, air_purifier.get_state())

    @mock.patch('subprocess.call', cmd_call_false_for_off_button)
    def test_switch_on_success_switch_off_failure(self):
        air_purifier = AirPurifier(MockedConfig())
        self.assertTrue(air_purifier.turn_on())
        self.assertEqual(1, air_purifier.get_state())
        self.assertFalse(air_purifier.turn_off())
        self.assertEqual(1, air_purifier.get_state())

    @mock.patch('subprocess.call', cmd_call_false_for_on_button)
    def test_switch_off_success_switch_on_failure(self):
        air_purifier = AirPurifier(MockedConfig())
        self.assertTrue(air_purifier.turn_off())
        self.assertEqual(0, air_purifier.get_state())
        self.assertFalse(air_purifier.turn_on())
        self.assertEqual(0, air_purifier.get_state())

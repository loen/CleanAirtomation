import unittest

from unittest.mock import MagicMock

from CleanAirtomation import CleanAirtomationService
from CleanAirtomation.AirPurifier import AirPurifier
from CleanAirtomation.AirlyDao import AirlyDao


class ConfigMock:

    def read_config(self):
        return {'commandPath': 'cmd',
                'onButtonMac': 'FF:AA:CC',
                'offButtonMac': 'OO:12:34'}


class CleanAirtomationServiceTest(unittest.TestCase):

    def test_air_purifier_not_touched_on_airly_error(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=None)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        clean_airtomation_service = CleanAirtomationService.CleanAirtomationService(70, airily_dao, air_purifier)
        # test
        clean_airtomation_service.clean_polluted_air()

        # verify
        airily_dao.caqi.assert_called_once()
        air_purifier.turn_off.assert_not_called()
        air_purifier.turn_on.assert_not_called()

    def test_turn_on_purifier(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=100)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        clean_airtomation_service = CleanAirtomationService.CleanAirtomationService(70, airily_dao, air_purifier)
        # test
        clean_airtomation_service.clean_polluted_air()

        # verify
        airily_dao.caqi.assert_called_once()
        air_purifier.turn_off.assert_not_called()
        air_purifier.turn_on.assert_called_once()

    def test_turn_off_purifier(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=60)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.get_state = MagicMock(return_value=1)
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        clean_airtomation_service = CleanAirtomationService.CleanAirtomationService(70, airily_dao, air_purifier)
        # test
        clean_airtomation_service.clean_polluted_air()

        # verify
        airily_dao.caqi.assert_called_once()
        air_purifier.turn_on.assert_not_called()
        air_purifier.turn_off.assert_called_once()

    def test_double_turn_on(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=100)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        clean_airtomation_service = CleanAirtomationService.CleanAirtomationService(70, airily_dao, air_purifier)

        # test
        clean_airtomation_service.clean_polluted_air()
        air_purifier.get_state = MagicMock(return_value=1)
        clean_airtomation_service.clean_polluted_air()

        # verify
        air_purifier.turn_on.assert_called_once()
        air_purifier.turn_off.assert_not_called()

    def test_double_turn_off(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=10)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=1)
        clean_airtomation_service = CleanAirtomationService.CleanAirtomationService(70, airily_dao, air_purifier)

        # test
        clean_airtomation_service.clean_polluted_air()
        air_purifier.get_state = MagicMock(return_value=0)
        clean_airtomation_service.clean_polluted_air()

        # verify
        air_purifier.turn_on.assert_not_called()
        air_purifier.turn_off.assert_called_once()

    def test_on_and_off(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=100)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=0)
        clean_airtomation_service = CleanAirtomationService.CleanAirtomationService(70, airily_dao, air_purifier)

        # test
        clean_airtomation_service.clean_polluted_air()
        air_purifier.get_state = MagicMock(return_value=1)
        airily_dao.caqi = MagicMock(return_value=10)
        clean_airtomation_service.clean_polluted_air()

        # verify
        air_purifier.turn_on.assert_called_once()
        air_purifier.turn_off.assert_called_once()

    def test_off_and_on(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=10)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=1)
        clean_airtomation_service = CleanAirtomationService.CleanAirtomationService(70, airily_dao, air_purifier)

        # test
        clean_airtomation_service.clean_polluted_air()
        air_purifier.get_state = MagicMock(return_value=0)
        airily_dao.caqi = MagicMock(return_value=100)
        clean_airtomation_service.clean_polluted_air()

        # verify
        air_purifier.turn_on.assert_called_once()
        air_purifier.turn_off.assert_called_once()

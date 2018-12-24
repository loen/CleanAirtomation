import unittest
from freezegun import freeze_time

from unittest.mock import MagicMock

from clean_airtomation.air_purifier import AirPurifier, AirPurifierState
from clean_airtomation.airly_dao import AirlyDao
from clean_airtomation.clean_airtomation_service import CleanAirtomationService


class ConfigMock:

    def read_config(self):
        return {'commandPath': 'cmd',
                'onButtonMac': 'FF:AA:CC',
                'offButtonMac': 'OO:12:34',
                }


class CleanAirtomationServiceTest(unittest.TestCase):

    def get_cleaning_pause(self, days, startTime, endTime):
        return {'days': days,
                'startTime': startTime,
                'endTime': endTime}

    @freeze_time("2018-12-12 21:00:00")
    def test_air_purifier_not_touched_on_airly_error(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=None)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)
        # test
        clean_airtomation_service.clean_polluted_air()

        # verify
        airily_dao.caqi.assert_called_once()
        air_purifier.turn_off.assert_not_called()
        air_purifier.turn_on.assert_not_called()

    @freeze_time("2018-12-12 21:00:00")
    def test_turn_on_purifier(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=100)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)
        # test
        clean_airtomation_service.clean_polluted_air()

        # verify
        airily_dao.caqi.assert_called_once()
        air_purifier.turn_off.assert_not_called()
        air_purifier.turn_on.assert_called_once()

    @freeze_time("2018-12-12 21:00:00")
    def test_turn_off_purifier(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=60)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.ON)
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)
        # test
        clean_airtomation_service.clean_polluted_air()

        # verify
        airily_dao.caqi.assert_called_once()
        air_purifier.turn_on.assert_not_called()
        air_purifier.turn_off.assert_called_once()

    @freeze_time("2018-12-12 21:00:00")
    def test_double_turn_on(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=100)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)

        # test
        clean_airtomation_service.clean_polluted_air()
        air_purifier.get_state = MagicMock(return_value=1)
        clean_airtomation_service.clean_polluted_air()

        # verify
        air_purifier.turn_on.assert_called_once()
        air_purifier.turn_off.assert_not_called()

    @freeze_time("2018-12-12 21:00:00")
    def test_double_turn_off(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=10)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.ON)
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)

        # test
        clean_airtomation_service.clean_polluted_air()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.OFF)
        clean_airtomation_service.clean_polluted_air()

        # verify
        air_purifier.turn_on.assert_not_called()
        air_purifier.turn_off.assert_called_once()

    @freeze_time("2018-12-12 21:00:00")
    def test_on_and_off(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=100)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.OFF)
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)

        # test
        clean_airtomation_service.clean_polluted_air()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.ON)
        airily_dao.caqi = MagicMock(return_value=10)
        clean_airtomation_service.clean_polluted_air()

        # verify
        air_purifier.turn_on.assert_called_once()
        air_purifier.turn_off.assert_called_once()

    @freeze_time("2018-12-12 21:00:00")
    def test_off_and_on(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=10)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.ON)
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)

        # test
        clean_airtomation_service.clean_polluted_air()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.OFF)
        airily_dao.caqi = MagicMock(return_value=100)
        clean_airtomation_service.clean_polluted_air()

        # verify
        air_purifier.turn_on.assert_called_once()
        air_purifier.turn_off.assert_called_once()

    @freeze_time("2018-12-12 11:22:00")
    def test_in_pause(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=10)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.ON)
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)

        # test
        result = clean_airtomation_service._is_not_in_pause_time()

        # verify
        self.assertFalse(result)

    @freeze_time("2018-12-13 11:00:00")
    def test_not_pause_day(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=10)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.ON)
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)
        # test
        result = clean_airtomation_service._is_not_in_pause_time()

        # verify
        self.assertTrue(result)

    @freeze_time("2018-12-12 7:00:00")
    def test_not_pause_hour_less(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=10)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.ON)
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)
        # test
        result = clean_airtomation_service._is_not_in_pause_time()

        # verify
        self.assertTrue(result)

    @freeze_time("2018-12-12 17:00:00")
    def test_not_pause_hour_more(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=10)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.ON)
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)
        # test
        result = clean_airtomation_service._is_not_in_pause_time()

        # verify
        self.assertTrue(result)

    @freeze_time("2018-12-12 8:00:00")
    def test_pause_edge_left(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=10)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.ON)
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)
        # test
        result = clean_airtomation_service._is_not_in_pause_time()

        # verify
        self.assertFalse(result)

    @freeze_time("2018-12-12 16:00:00")
    def test_pause_edge_right(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=10)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.turn_on = MagicMock()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.ON)
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)
        # test
        result = clean_airtomation_service._is_not_in_pause_time()

        # verify
        self.assertFalse(result)

    @freeze_time("2018-12-12 9:00:00")
    def test_pause_period_before_on(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=80)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.ON)
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)
        # test
        clean_airtomation_service.clean_polluted_air()

        # verify
        airily_dao.caqi.assert_not_called()
        air_purifier.turn_off.assert_called_once()

    @freeze_time("2018-12-12 9:00:00")
    def test_pause_period_before_off(self):
        # setup
        airily_dao = AirlyDao('url', 'key', 28)
        airily_dao.caqi = MagicMock(return_value=80)
        air_purifier = AirPurifier(ConfigMock())
        air_purifier.turn_off = MagicMock()
        air_purifier.get_state = MagicMock(return_value=AirPurifierState.OFF)
        cleaning_pause = self.get_cleaning_pause(['Monday', 'Tuesday', 'Wednesday'], '8:00', '16:00')
        clean_airtomation_service = CleanAirtomationService(70, cleaning_pause, airily_dao,
                                                            air_purifier)
        # test
        clean_airtomation_service.clean_polluted_air()

        # verify
        airily_dao.caqi.assert_not_called()
        air_purifier.turn_off.assert_not_called()


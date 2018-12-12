import calendar
import datetime
import logging
from logging.config import fileConfig


class CleanAirtomationService:

    def __init__(self, caqi_treshold, cleaning_pause, airly_dao, air_purifier):
        self.airly_dao = airly_dao
        self.air_purifier = air_purifier
        self.caqi_treshold = caqi_treshold
        self.cleaning_pause = cleaning_pause
        fileConfig('logging_config.ini')
        self.logger = logging.getLogger()

    def clean_polluted_air(self):
        if self.is_not_in_pause_time():
            current_caqi = self.airly_dao.caqi()
            self.logger.info('current caqi value: %s', str(current_caqi))
            if current_caqi is not None:
                if current_caqi > self.caqi_treshold:
                    self.logger.debug('CAQI above treshold, state of purifier = %d', self.air_purifier.get_state())
                    if self.air_purifier.get_state() == 0:
                        self.logger.info('bad air - purifier needs to be switched on')
                        on_status = self.air_purifier.turn_on()
                        self.logger.info('air purifier turn on with status: %s', str(on_status))
                else:
                    self.logger.info('CAQI below treshold, state of purifier = %d', self.air_purifier.get_state())
                    if self.air_purifier.get_state() == 1:
                        self.logger.info('good air - purifier needs to be switched off')
                        off_status = self.air_purifier.turn_off()
                        self.logger.info('air purifier turn off with status: %s' + str(off_status))
            else:
                self.logger.info('Unable to get CAQI from Airly')
        else:
            self.logger.info('Pause period - air purifier needs to be switched off')
            if self.air_purifier.get_state == 1:
                self.air_purifier.turn_off()

    def is_not_in_pause_time(self):
        weekdays = self.cleaning_pause['days']
        start_hour = datetime.datetime.strptime(self.cleaning_pause['startTime'], "%H:%M")
        end_hour = datetime.datetime.strptime(self.cleaning_pause['endTime'], "%H:%M")
        current_day = calendar.day_name[datetime.datetime.today().weekday()]
        if current_day in weekdays:
            now = datetime.datetime.now()
            now_minutes_hours = start_hour.replace(hour=now.hour, minute=now.minute)
            if start_hour <= now_minutes_hours <= end_hour:
                return False
        return True

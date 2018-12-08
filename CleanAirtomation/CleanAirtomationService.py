import logging
from logging.config import fileConfig

class CleanAirtomationService:

    def __init__(self, caqi_treshold, airly_dao, air_purifier):
        self.airly_dao = airly_dao
        self.air_purifier = air_purifier
        self.caqi_treshold = caqi_treshold
        fileConfig('logging_config.ini')
        self.logger = logging.getLogger()

    def clean_polluted_air(self):
        current_caqi = self.airly_dao.caqi()
        self.logger.info('current caqi value: %d', current_caqi)
        if current_caqi is not None:
            if current_caqi > self.caqi_treshold:
                self.logger.debug('CAQI above treshold, state of purifier = %d', self.air_purifier.get_state())
                if self.air_purifier.get_state() == 0:
                    self.logger.info('bad air - purifier needs to be switched on')
                    on_status = self.air_purifier.turn_on()
                    self.logger.info('air purifier turn on with status: %d', on_status)

            else:
                self.logger.info('CAQI below treshold, state of purifier = %d', self.air_purifier.get_state())
                if self.air_purifier.get_state() == 1:
                    self.logger.info('good air - purifier needs to be switched off')
                    off_status = self.air_purifier.turn_off()
                    self.logger.info('air purifier turn off with status: %d' + off_status)
        else:
            self.logger.info('Unable to get CAQI from Airly')

import time

from clean_airtomation.air_purifier import AirPurifier
from clean_airtomation.airly_dao import AirlyDao
from clean_airtomation.calendar_dao import CalendarDao
from clean_airtomation.clean_airtomation_service import CleanAirtomationService
from clean_airtomation.config import Config

config = Config()
conf = config.read_config()
airly_dao = AirlyDao(conf['airlyUrl'], conf['apikey'], conf['installationId'])
air_purifier = AirPurifier(config)
calendar_dao = CalendarDao(conf['calendarUrl'])
cleanAirtomationService = CleanAirtomationService(conf['caqiTreshold'], conf['cleaningPause'],
                                                  airly_dao, calendar_dao, air_purifier)
while True:
    cleanAirtomationService.clean_polluted_air()
    time.sleep(conf['checkIntervalInMinutes'] * 60)


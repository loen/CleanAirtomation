import time

from clean_airtomation import CleanAirtomationService, AirlyDao, AirPurifier
from clean_airtomation.Config import Config

config = Config()
conf = config.read_config()
airly_dao = AirlyDao.AirlyDao(conf['airlyUrl'], conf['apikey'], conf['installationId'])
air_purifier = AirPurifier.AirPurifier(config)
cleanAirtomationService = CleanAirtomationService.CleanAirtomationService(conf['caqiTreshold'], conf['cleaningPause'], airly_dao, air_purifier)
while True:
    cleanAirtomationService.clean_polluted_air()
    time.sleep(conf['checkIntervalInMinutes'] * 60)


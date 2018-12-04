import time

from CleanAirtomation import CleanAirtomationService
from CleanAirtomation.Config import Config

config = Config()
check_interval_min = config.read_config()['checkIntervalInMinutes']
cleanAirtomationService = CleanAirtomationService.CleanAirtomationService(config)
while True:
    cleanAirtomationService.clean_polluted_air()
    time.sleep(check_interval_min * 60)


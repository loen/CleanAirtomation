from CleanAirtomation import CleanAirtomationService
from CleanAirtomation.Config import Config

config = Config()
cleanAirtomationService = CleanAirtomationService.CleanAirtomationService(config)
cleanAirtomationService.clean_polluted_air()


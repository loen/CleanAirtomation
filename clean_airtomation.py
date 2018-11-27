from CleanAirtomation.AirlyDao import AirlyDao
from CleanAirtomation.Config import Config
from CleanAirtomation.SwitchBotConnector import SwitchBotConnector

config = Config()
conf = config.read_config()
airly_dao = AirlyDao(conf['apikey'], conf['installationId'])
print(airly_dao.caqi())
switchBotConnector = SwitchBotConnector(conf['commandPath'], conf['mac'])
result = switchBotConnector.push_the_button()
print(result)


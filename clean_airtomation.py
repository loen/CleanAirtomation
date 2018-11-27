from CleanAirtomation.AirlyDao import AirlyDao
from CleanAirtomation.Config import Config

config = Config()
conf = config.read_config()
airly_dao = AirlyDao(conf['apikey'], conf['installationId'])
print(airly_dao.caqi())


import requests
import yaml

from CleanAirtomation.AirlyDao import AirlyDao
from CleanAirtomation.Config import Config

config = Config(yaml)
conf = config.read_config()
airly_dao = AirlyDao(requests, conf['apikey'], conf['installationId'])
print(airly_dao.caqi())


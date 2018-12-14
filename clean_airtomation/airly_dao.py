import logging
from logging.config import fileConfig

import requests


class AirlyDao:

    def __init__(self, airly_url, api_key, installation_id):
        self.airly_ulr = airly_url
        self.apiKey = api_key
        self.installationId = installation_id
        fileConfig('logging_config.ini')
        self.logger = logging.getLogger()

    def caqi(self):
        try:
            response = requests.get(
                self.airly_ulr + '/v2/measurements/installation?installationId=' + str(self.installationId),
                headers={'Accept': 'application/json', 'apikey': self.apiKey})

            if response.status_code == 200:
                resp = response.json()
                return resp['current']['indexes'][0]['value']
            else:
                return None
        except requests.exceptions.RequestException:
            self.logger.info('Unable to connect to airapi.airly.eu')
            return None

import requests


class AirlyDao:

    def __init__(self, api_key, installation_id):
        self.apiKey = api_key
        self.installationId = installation_id

    def caqi(self):
        response = requests.get(
            'https://airapi.airly.eu/v2/measurements/installation?installationId=' + str(self.installationId),
            headers={'Accept': 'application/json', 'apikey': self.apiKey})
        resp = response.json()
        return resp['current']['indexes'][0]['value']

import requests


class AirlyDao:

    def __init__(self, api_key, installation_id):
        self.apiKey = api_key
        self.installationId = installation_id

    def caqi(self):
        try:
            response = requests.get(
                'https://airapi.airly.eu/v2/measurements/installation?installationId=' + str(self.installationId),
                headers={'Accept': 'application/json', 'apikey': self.apiKey})
            if response.status_code == 200:
                resp = response.json()
                return resp['current']['indexes'][0]['value']
            else:
                return None
        except requests.exceptions.RequestException:
            print('Unable to connect to airapi.airly.eu')
            return None

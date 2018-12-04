import yaml


class Config:

    def read_config(self):
        with open("config.yaml", 'r') as stream:
            data_loaded = yaml.load(stream)
            return {'installationId': data_loaded['installationId'],
                    'airlyUrl': data_loaded['airlyUrl'],
                    'apikey': data_loaded['apikey'],
                    'commandPath': data_loaded['commandPath'],
                    'onButtonMac': data_loaded['onButtonMac'],
                    'offButtonMac': data_loaded['offButtonMac'],
                    'caqiTreshold': data_loaded['caqiTreshold'],
                    'checkIntervalInMinutes': data_loaded['checkIntervalInMinutes']}

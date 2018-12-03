import yaml


class Config:

    def read_config(self):
        with open("config.yaml", 'r') as stream:
            data_loaded = yaml.load(stream)
            return {'installationId': data_loaded['installationId'],
                    'apikey': data_loaded['apikey'],
                    'commandPath': data_loaded['commandPath'],
                    'on_button_mac': data_loaded['on_button_mac'],
                    'off_button_mac': data_loaded['off_button_mac']}

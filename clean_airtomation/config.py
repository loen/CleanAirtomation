import os

import yaml


class Config:

    def read_config(self, base_dir=None):
        config_path = "config.yaml"
        if base_dir:
            config_path = os.path.join(base_dir, config_path)

        with open(config_path, 'r') as stream:
            data_loaded = yaml.load(stream)
            return {'installationId': data_loaded['installationId'],
                    'airlyUrl': data_loaded['airlyUrl'],
                    'apikey': data_loaded['apikey'],
                    'commandPath': data_loaded['commandPath'],
                    'onButtonMac': data_loaded['onButtonMac'],
                    'offButtonMac': data_loaded['offButtonMac'],
                    'caqiTreshold': data_loaded['caqiTreshold'],
                    'checkIntervalInMinutes': data_loaded['checkIntervalInMinutes'],
                    'cleaningPause': data_loaded['cleaningPause']}

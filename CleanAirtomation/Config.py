import yaml


class Config:

    def __init__(self, yaml):
        self.yaml = yaml

    def read_config(self):
        with open("config.yaml", 'r') as stream:
            data_loaded = yaml.load(stream)
            return {'installationId': data_loaded['installationId'], 'apikey': data_loaded['apikey']}

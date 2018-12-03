from CleanAirtomation import SwitchBotConnector


class AirPurifier:

    def __init__(self, config):
        conf = config.read_config()
        self.on_button = SwitchBotConnector.SwitchBotConnector(conf['commandPath'], conf['onButtonMac'])
        self.off_button = SwitchBotConnector.SwitchBotConnector(conf['commandPath'], conf['offButtonMac'])
        self.state = 0

    def turn_on(self):
        result = self.on_button.push_the_button()
        if result:
            self.state = 1
            return True
        else:
            return False

    def turn_off(self):
        result = self.off_button.push_the_button()
        if result:
            self.state = 0
            return True
        else:
            return False

    def get_state(self):
        return self.state

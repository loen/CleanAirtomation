from enum import Enum, auto

from clean_airtomation.config import Config
from clean_airtomation.switch_bot_connector import SwitchBotConnector


class AirPurifierState(Enum):
    ON = auto()
    OFF = auto()


class AirPurifier:

    def __init__(self, config: Config):
        conf = config.read_config()
        self.on_button = SwitchBotConnector(conf['commandPath'], conf['onButtonMac'])
        self.off_button = SwitchBotConnector(conf['commandPath'], conf['offButtonMac'])
        self.state = AirPurifierState.OFF

    def turn_on(self) -> bool:
        result = self.on_button.push_the_button()
        if result:
            self.state = AirPurifierState.ON
            return True
        else:
            return False

    def turn_off(self):
        result = self.off_button.push_the_button()
        if result:
            self.state = AirPurifierState.OFF
            return True
        else:
            return False

    def get_state(self) -> AirPurifierState:
        return self.state

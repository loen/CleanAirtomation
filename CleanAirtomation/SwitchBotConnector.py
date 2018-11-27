from subprocess import call


class SwitchBotConnector:

    def __init__(self, command_path, mac):
        self.command_path = command_path
        self.mac = mac

    def push_the_button(self):
        ret = call(['sudo', 'python', self.command_path, self.mac, "Press"])
        if ret == 0:
            return True
        else:
            return False

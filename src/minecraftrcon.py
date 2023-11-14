import mcrcon
import os
from src.config import Config

class MinecraftRcon:
    def __init__(self):
        self.config = Config(os.path.join(os.path.dirname(__file__), "../config.yml"))
        self.rcon = mcrcon.MCRcon(self.config.getRCONHost(), self.config.getRCONPassword(), self.config.getRCONPort())

    def send_command(self, command):
        self.rcon.connect()
        resp = self.rcon.command(command)
        self.rcon.disconnect()
        return resp
    
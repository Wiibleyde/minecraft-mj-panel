import logging
import os

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    white = "\x1b[37;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s %(message)s"

    FORMATS = {
        logging.DEBUG: white + format + reset,
        logging.INFO: white + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    def __init__(self,filePath="./logs/logs.log", withConsole=True):
        if not os.path.exists(os.path.dirname(filePath)):
            os.makedirs(os.path.dirname(filePath))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = CustomFormatter()
        file_handler = logging.FileHandler(filePath)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        if withConsole:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def emergency(self,message):
        self.logger.critical(message)

    def alert(self,message):
        self.logger.critical(message)

    def critical(self,message):
        self.logger.critical(message)

    def error(self,message):
        self.logger.error(message)

    def warning(self,message):
        self.logger.warning(message)

    def notice(self,message):
        self.logger.info(message)

    def info(self,message):
        self.logger.info(message)

    def debug(self,message):
        self.logger.debug(message)

from c_discord_webhook import send_msg
import logging


def get_logger(name):
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler()
    d_handler = logging.FileHandler('Logs/debug.log')
    e_handler = logging.FileHandler('Logs/error.log')
    c_handler.setLevel(logging.INFO)
    d_handler.setLevel(logging.DEBUG)
    e_handler.setLevel(logging.ERROR)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    d_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    e_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    d_handler.setFormatter(d_format)
    e_handler.setFormatter(e_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(d_handler)
    logger.addHandler(e_handler)
    return logger


class ActivityLogger:
    def __init__(self, name):
        self.logger = get_logger(name)

    def log_event_debug(self, message):
        self.logger.debug(message)

    def log_event_info(self, message, discord=()):
        self.logger.info(message)
        if discord:
            # print(discord)
            send_msg(*discord)

    def log_event_warn(self, message, discord=()):
        self.logger.warning(message)
        if discord:
            send_msg(*discord)

    def log_event_error(self, message, exception=None, discord=()):
        self.logger.error(message)
        if exception:
            self.logger.exception(exception)
        if discord:
            send_msg(*discord)

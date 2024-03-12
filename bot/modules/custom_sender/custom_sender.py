from .driver import BotDriver
from .engine import BotEngine
from .methods import Methods


class CustomSender:
    def __init__(self):
        self.engine = BotEngine()
        self.driver = BotDriver(self.engine)
        self.methods = Methods(self.driver)

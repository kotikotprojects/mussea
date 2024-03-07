from .content import Content
from .driver import TikTokDriver
from .engine import TikTokEngine


class TikTok:
    def __init__(self):
        self.engine = TikTokEngine()
        self.driver = TikTokDriver(engine=self.engine)
        self.content = Content(driver=self.driver)

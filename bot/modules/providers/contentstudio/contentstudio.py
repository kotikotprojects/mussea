from .engine import ContentStudioEngine
from .driver import ContentStudioDriver
from .content import Content


class ContentStudio:
    def __init__(self):
        self.engine = ContentStudioEngine()
        self.driver = ContentStudioDriver(engine=self.engine)
        self.content = Content(driver=self.driver)

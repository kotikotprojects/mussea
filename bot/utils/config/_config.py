import tomllib


class Config(dict):
    def __init__(self, _config: dict = None):
        try:
            if _config is None:
                super().__init__(**tomllib.load(open("config.toml", "rb")))
            else:
                super().__init__(**_config)

        except FileNotFoundError:
            super().__init__()

    def __getattr__(self, item):
        if not isinstance(self.get(item), dict):
            return self.get(item)
        else:
            return self.__class__(_config=self.get(item))

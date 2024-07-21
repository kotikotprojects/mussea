from dataclasses import dataclass

from .common.providers import Provider
from .contentstudio import contentstudio
from .estimator import estimator
from .tiktokapi import tiktokapi


class NoProvidersLeft(Exception):
    pass


@dataclass
class Providers:
    __providers = [estimator, tiktokapi, contentstudio]
    __current = -1

    def get_next(self) -> Provider:
        self.__current += 1
        try:
            return self.__providers[self.__current]
        except IndexError:
            raise NoProvidersLeft()

    def get_for_type(self, supports):
        try:
            self.__current += 1
            current = self.__providers[self.__current]
        except IndexError:
            raise NoProvidersLeft()
        while not getattr(current, f"supports_{supports}", False):
            self.__current += 1
            try:
                current = self.__providers[self.__current]
            except IndexError:
                raise NoProvidersLeft()

        return current

    def get_for_video(self) -> Provider:
        return self.get_for_type("video")

    def get_for_audio(self) -> Provider:
        return self.get_for_type("audio")

    def get_for_photos(self) -> Provider:
        return self.get_for_type("photos")

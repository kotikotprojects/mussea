from urllib.parse import urlparse

from aiogram.filters import BaseFilter
from aiogram.types import Message


class TikTokUrlFilter(BaseFilter):
    @staticmethod
    def get_tiktoks(message: Message):
        tiktoks = list()
        entities = message.entities or []
        for item in entities:
            if item.type == "url":
                url = urlparse(item.extract_from(message.text))
                if url.scheme in ["http", "https"] and url.netloc.endswith(
                    "tiktok.com"
                ):
                    tiktoks.append(url.geturl())

        return tiktoks

    async def __call__(self, message: Message):
        return TikTokUrlFilter.get_tiktoks(message)

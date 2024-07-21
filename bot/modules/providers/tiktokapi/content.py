import re
from typing import Optional

from attrs import define

from ..common.content import BasePhotos, BaseVideo
from .driver import TikTokDriver

REGEX_VIDEO_ID = (
    r"(?:https:\/\/(?:www\.)*tiktok\.com\/@[^?\/]+\/video\/)(?:([0-9]+)?(?:\?.+)?$|$)"
)
REGEX_PHOTO_ID = (
    r"(?:https:\/\/(?:www\.)*tiktok\.com\/@[^?\/]+\/photo\/)(?:([0-9]+)?(?:\?.+)?$|$)"
)
REGEX_TIKTOK_URL = (
    r"(https:\/\/(?:www\.)*tiktok\.com\/@[^?\/]+)"
    r"(?:(\/(?:video|photo)\/[0-9]+)?(\?.+)?$|$)"
)


@define
class TikTokVideo(BaseVideo):
    @classmethod
    async def from_detail_json(cls, data: dict):
        return cls(url=data["video"]["playAddr"])


@define
class TikTokPhotos(BasePhotos):
    @classmethod
    async def from_detail_json(cls, data: dict, driver: TikTokDriver):
        ready_urls = list()
        images = data["imagePost"]["images"]
        for image in images:
            ready_urls.append(image["imageURL"]["urlList"][0])

        try:
            added_song = data["music"]["playUrl"]
            if await driver.engine.check_exists(added_song):
                return cls(urls=ready_urls, audio_url=added_song)
            else:
                raise TypeError

        except (TypeError, AttributeError, IndexError):
            return cls(urls=ready_urls, audio_url=None)


@define
class Content:
    driver: TikTokDriver

    async def from_id(self, aweme_id: str) -> Optional[TikTokVideo | TikTokPhotos]:
        r = await self.driver.get_detail(aweme_id)

        if r is None:
            return None

        if r.get("imagePost"):
            return await TikTokPhotos.from_detail_json(r, self.driver)
        elif r.get("video"):
            return await TikTokVideo.from_detail_json(r)

        else:
            return None

    async def from_url(self, url: str) -> Optional[TikTokVideo | TikTokPhotos]:
        url_ = re.search(REGEX_TIKTOK_URL, url, re.IGNORECASE)
        if not url_:
            url_ = await self.driver.engine.real_url(url)
            url = re.search(REGEX_TIKTOK_URL, url_, re.IGNORECASE)
        else:
            url = url_

        if not url:
            return None

        return await self.from_id(url.groups()[1].split("/")[-1])

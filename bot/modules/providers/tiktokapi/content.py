import re
import urllib.parse
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
    async def from_aweme_json(cls, data: dict, driver: TikTokDriver):
        urls = data["video"]["play_addr"]["url_list"]
        for url in urls:
            url = urllib.parse.urlparse(url)
            url = f"{url.scheme}://{url.netloc}{url.path}"
            if await driver.engine.check_exists(url):
                return cls(url=url)


@define
class TikTokPhotos(BasePhotos):
    @classmethod
    async def from_aweme_json(cls, data: dict, driver: TikTokDriver):
        ready_urls = list()
        images = data["image_post_info"]["images"]
        for image in images:
            urls = image["display_image"]["url_list"]
            for url in urls:
                if await driver.engine.check_exists(url):
                    ready_urls.append(url)
                    break

        try:
            added_songs = data["added_sound_music_info"]["play_url"]["url_list"]
            for song in added_songs:
                if await driver.engine.check_exists(song):
                    return cls(urls=ready_urls, audio_url=song)
                else:
                    raise TypeError

        except (TypeError, AttributeError, IndexError):
            return cls(urls=ready_urls, audio_url=None)


@define
class Content:
    driver: TikTokDriver

    async def from_id(self, aweme_id: str) -> Optional[TikTokVideo | TikTokPhotos]:
        r = await self.driver.get_aweme(aweme_id)

        if r is None:
            return None

        try:
            if r["content_type"] == "video":
                return await TikTokVideo.from_aweme_json(r, self.driver)
            elif "photo" in r["content_type"]:
                return await TikTokPhotos.from_aweme_json(r, self.driver)

            else:
                return None

        except KeyError:
            if r.get("image_post_info"):
                return await TikTokPhotos.from_aweme_json(r, self.driver)
            elif r.get("video"):
                return await TikTokVideo.from_aweme_json(r, self.driver)

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

from async_lru import alru_cache

from ..common.propagations import (
    PropagateAudioNeeded,
    PropagateEverythingNeeded,
    PropagatePhotosNeeded,
    PropagateVideoNeeded,
)
from ..common.providers import Provider
from .content import Content, TikTokPhotos, TikTokVideo
from .driver import TikTokDriver
from .engine import TikTokEngine


class TikTok(Provider):
    supports_video = True
    supports_audio = True
    supports_photos = True
    wants = "id"

    def __init__(self):
        self.engine = TikTokEngine()
        self.driver = TikTokDriver(engine=self.engine)
        self.content = Content(driver=self.driver)

    @alru_cache()
    async def from_id(
        self, url: str
    ) -> (
        TikTokVideo
        | TikTokPhotos
        | PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        return await self.content.from_id(url)

    @alru_cache()
    async def from_url(
        self, url: str
    ) -> (
        TikTokVideo
        | TikTokPhotos
        | PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        return await self.content.from_url(url)

    @alru_cache()
    async def from_preferred(
        self, preferred: str
    ) -> (
        TikTokVideo
        | TikTokPhotos
        | PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        return await self.from_id(preferred)

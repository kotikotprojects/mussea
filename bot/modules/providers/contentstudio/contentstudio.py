from async_lru import alru_cache

from ..common.propagations import (
    PropagateAudioNeeded,
    PropagateEverythingNeeded,
    PropagatePhotosNeeded,
    PropagateVideoNeeded,
)
from ..common.providers import Provider
from .content import Content, ContentStudioVideo
from .driver import ContentStudioDriver
from .engine import ContentStudioEngine


class ContentStudio(Provider):
    supports_video = True
    supports_audio = True
    supports_photos = False
    wants = "url"

    def __init__(self):
        self.engine = ContentStudioEngine()
        self.driver = ContentStudioDriver(engine=self.engine)
        self.content = Content(driver=self.driver)

    @alru_cache()
    async def from_url(
        self, url: str
    ) -> (
        ContentStudioVideo
        | PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        return await self.content.from_url(url)

    @alru_cache()
    async def from_id(
        self, url: str
    ) -> (
        ContentStudioVideo
        | PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        return await self.content.from_id(url)

    @alru_cache()
    async def from_preferred(
        self, preferred: str
    ) -> (
        ContentStudioVideo
        | PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        return await self.from_url(preferred)

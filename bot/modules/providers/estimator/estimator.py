from async_lru import alru_cache

from ..common.engine import CommonEngine
from ..common.propagations import (
    PropagateAudioNeeded,
    PropagateEverythingNeeded,
    PropagatePhotosNeeded,
    PropagateVideoNeeded,
)
from ..common.providers import Provider
from .content import Content


class Estimator(Provider):
    supports_video = True
    supports_audio = True
    supports_photos = True
    wants = "url"

    def __init__(self):
        self.engine = CommonEngine()
        self.content = Content(engine=self.engine)

    @alru_cache()
    async def from_url(
        self, url: str
    ) -> (
        PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        return await self.content.from_url(url)

    @alru_cache()
    async def from_id(
        self, url: str
    ) -> (
        PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        return await self.content.from_id(url)

    @alru_cache()
    async def from_preferred(
        self, preferred: str
    ) -> (
        PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        return await self.from_url(preferred)

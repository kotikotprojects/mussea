from abc import ABC, abstractmethod
from typing import Literal

from .content import BasePhotos, BaseVideo
from .propagations import (
    PropagateAudioNeeded,
    PropagateEverythingNeeded,
    PropagatePhotosNeeded,
    PropagateVideoNeeded,
)


class Provider(ABC):
    supports_video: bool
    supports_audio: bool
    supports_photos: bool
    wants: Literal["url", "id"]

    @abstractmethod
    async def from_url(
        self, url: str
    ) -> (
        BaseVideo
        | BasePhotos
        | PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        pass

    @abstractmethod
    async def from_id(
        self, url: str
    ) -> (
        BaseVideo
        | BasePhotos
        | PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        pass

    @abstractmethod
    async def from_preferred(
        self, preferred: str
    ) -> (
        BaseVideo
        | BasePhotos
        | PropagateEverythingNeeded
        | PropagateAudioNeeded
        | PropagateVideoNeeded
        | PropagatePhotosNeeded
    ):
        pass

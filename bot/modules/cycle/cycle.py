from dataclasses import dataclass, field

from ..providers import Providers
from ..providers.common.content import BasePhotos, BaseVideo
from ..providers.common.propagations import (
    PropagateAudioNeeded,
    PropagateEverythingNeeded,
    PropagatePhotosNeeded,
    PropagateVideoNeeded,
)


@dataclass
class Jobs:
    __job = None

    @property
    def estimate(self) -> bool:
        return self.__job == "estimate"

    def set_estimate(self):
        self.__job = "estimate"

    @property
    def send(self) -> bool:
        return self.__job == "send"

    def set_send(self):
        self.__job = "send"


@dataclass
class LinkCycle:
    url: str
    id: str = None

    providers: Providers = field(default_factory=Providers)

    estimated = None

    job: Jobs = field(default_factory=Jobs)
    needs: PropagatePhotosNeeded | PropagateVideoNeeded | PropagateEverythingNeeded | PropagateAudioNeeded = (
        None
    )

    video: BaseVideo = None
    photos: BasePhotos = None
    audio: str = None

    finished: bool = False
    end_error: bool = False

    can_propagate = ["id", "video", "photos", "audio"]

    def set_estimate(self):
        self.job.set_estimate()
        return self

    def set_finished(self):
        self.finished = True

    def set_error(self):
        self.end_error = True

from dataclasses import dataclass
from typing import Optional


@dataclass
class PropagatePhotosNeeded:
    audio: str
    id: Optional[str] = None
    needs = "photos"


@dataclass
class PropagateVideoNeeded:
    id: Optional[str] = None
    needs = "video"


@dataclass
class PropagateAudioNeeded:
    photos: list[str]
    id: Optional[str] = None
    needs = "audio"


@dataclass
class PropagateEverythingNeeded:
    id: Optional[str] = None
    needs = None

from dataclasses import dataclass


@dataclass
class PropagatePhotosNeeded:
    audio: str


@dataclass
class PropagateVideoNeeded:
    pass


@dataclass
class PropagateAudioNeeded:
    photos: list[str]


@dataclass
class PropagateEverythingNeeded:
    pass

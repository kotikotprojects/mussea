from typing import Optional

from attrs import define


@define
class BaseVideo:
    url: str


@define
class BasePhotos:
    urls: list[str]
    audio_url: Optional[str]
    audio_author: Optional[str]
    audio_title: Optional[str]

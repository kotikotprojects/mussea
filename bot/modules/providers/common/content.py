from typing import Optional, TypeVar

from attrs import define

T = TypeVar("T")


@define
class BaseVideo:
    url: str


@define
class BasePhotos:
    urls: list[str]
    audio_url: Optional[str]

    @staticmethod
    def get_chunked_list(lst: list[T], length: int) -> list[list[T]]:
        return [lst[i : i + length] for i in range(0, len(lst), length)]

    @property
    def urls_chunked(self, chunk_len: int = 10) -> list[list[str]]:
        return self.get_chunked_list(self.urls, chunk_len)

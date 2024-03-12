from typing import Optional

from attrs import define

from ..common.content import BaseVideo
from ..common.propagations import PropagatePhotosNeeded
from .driver import ContentStudioDriver


@define
class ContentStudioVideo(BaseVideo):
    @classmethod
    def from_url(cls, url: str):
        return cls(url=url)


@define
class Content:
    driver: ContentStudioDriver

    async def from_id(
        self, video_id: str
    ) -> Optional[ContentStudioVideo | PropagatePhotosNeeded]:
        return await self.from_url(f"https://www.tiktok.com/@/video/{video_id}")

    async def from_url(
        self, url: str
    ) -> Optional[ContentStudioVideo | PropagatePhotosNeeded]:
        url = await self.driver.get_url(url)

        if not isinstance(url, str):
            return None

        if url.endswith(".mp3") or "music" in url.split("/")[1]:
            return PropagatePhotosNeeded(audio=url)

        return ContentStudioVideo.from_url(url)

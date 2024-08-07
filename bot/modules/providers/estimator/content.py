import re
from typing import Optional

from attrs import define

from ..common.engine import CommonEngine
from ..common.propagations import (
    PropagateEverythingNeeded,
    PropagatePhotosNeeded,
    PropagateVideoNeeded,
)

REGEX_VIDEO_ID = (
    r"(?:https:\/\/(?:www\.)*tiktok\.com\/@[^?\/]+\/video\/)(?:([0-9]+)?(?:\?.+)?$|$)"
)
REGEX_PHOTO_ID = (
    r"(?:https:\/\/(?:www\.)*tiktok\.com\/@[^?\/]+\/photo\/)(?:([0-9]+)?(?:\?.+)?$|$)"
)
REGEX_TIKTOK_URL = (
    r"(https:\/\/(?:www\.)*tiktok\.com\/@[^?\/]+)"
    r"(?:(\/(?:video|photo)\/[0-9]+)?(\?.+)?$|$)"
)


@define
class Content:
    engine: CommonEngine

    @staticmethod
    async def from_id(video_id: str) -> Optional[PropagateEverythingNeeded]:
        return PropagateEverythingNeeded(video_id)

    async def from_url(
        self,
        url: str,
    ) -> Optional[
        PropagateVideoNeeded | PropagatePhotosNeeded | PropagateEverythingNeeded
    ]:
        if g := re.search(REGEX_VIDEO_ID, url, re.IGNORECASE):
            return PropagateVideoNeeded(id=g.groups()[0])
        elif g := re.search(REGEX_PHOTO_ID, url, re.IGNORECASE):
            return PropagatePhotosNeeded(id=g.groups()[0])
        elif g := re.search(REGEX_TIKTOK_URL, url, re.IGNORECASE):
            return PropagateEverythingNeeded(id=g.groups()[1].split("/")[-1])
        else:
            url = await self.engine.real_url(url)
            if g := re.search(REGEX_VIDEO_ID, url, re.IGNORECASE):
                return PropagateVideoNeeded(id=g.groups()[0])
            elif g := re.search(REGEX_PHOTO_ID, url, re.IGNORECASE):
                return PropagatePhotosNeeded(id=g.groups()[0])
            elif g := re.search(REGEX_TIKTOK_URL, url, re.IGNORECASE):
                return PropagateEverythingNeeded(id=g.groups()[1].split("/")[-1])
            else:
                return PropagateEverythingNeeded()

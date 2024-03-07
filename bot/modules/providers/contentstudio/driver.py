from attrs import define

from .engine import ContentStudioEngine


@define
class ContentStudioDriver:
    engine: ContentStudioEngine

    async def get_url(self, url: str):
        return (
            await self.engine.get(
                url="https://contentstudio.io/.netlify/functions/tiktokdownloaderapi",
                json={"url": url},
            )
        ).get("url")

import asyncio
from os import path

from attrs import define

from .engine import TikTokEngine

ENDPOINTS = [
    line.strip() for line in open(path.join(path.dirname(__file__), "endpoints"))
]
AWEME_APIS = [
    "https://" + point + suffix
    for point in ENDPOINTS
    for suffix in ["/aweme/v1/feed/", "/aweme/v1/aweme/detail/"]
]


@define
class TikTokDriver:
    engine: TikTokEngine

    async def get_aweme(self, aweme_id: str):
        tasks = [
            asyncio.create_task(
                self.engine.get(url=endpoint, params={"aweme_id": aweme_id})
            )
            for endpoint in AWEME_APIS
        ]
        while tasks:
            done, pending = await asyncio.wait(
                tasks, return_when=asyncio.FIRST_COMPLETED
            )

            tasks = list(pending)

            for task in done:
                if task.exception():
                    continue

                try:
                    data = await task
                    if data.get("aweme_list", [{}])[0].get("aweme_id") == aweme_id:
                        for remaining_task in tasks:
                            remaining_task.cancel()
                        return data["aweme_list"][0]

                except Exception as e:
                    assert e

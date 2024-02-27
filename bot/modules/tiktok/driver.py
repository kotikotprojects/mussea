from attrs import define

from .engine import TikTokEngine

AWEME_APIS = (
    "https://api19-core-c-useast1a.musical.ly/aweme/v1/feed/",
    "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/",
    "https://api31-normal-useast2a.tiktokv.com/aweme/v1/aweme/detail/",
)

STATIC_PARAMS = {
    "version_code": "330304",
    "app_name": "musical_ly",
    "channel": "App",
    "device_id": "null",
    "os_version": "16.6",
    "device_platform": "iphone",
    "device_type": "iPhone15",
}


@define
class TikTokDriver:
    engine: TikTokEngine

    async def get_aweme(self, aweme_id: str):
        for endpoint in AWEME_APIS:
            data = await self.engine.get(
                url=endpoint, params=STATIC_PARAMS | {"aweme_id": aweme_id}
            )
            try:
                if data["aweme_list"][0]["aweme_id"] == aweme_id:
                    return data["aweme_list"][0]
                else:
                    continue
            except (TypeError, AttributeError, IndexError):
                continue

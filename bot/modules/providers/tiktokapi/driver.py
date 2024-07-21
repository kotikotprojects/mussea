from attrs import define

from bot.utils.config import config

from .engine import TikTokEngine


@define
class TikTokDriver:
    engine: TikTokEngine

    async def get_detail(self, aweme_id: str):
        new_url = (
            await self.engine.post(
                config.tiktokapi.signer_microservice_url,
                data=f"https://www.tiktok.com/api/item/detail/"
                f"?WebIdLastTime=0&aid=1988&app_language=ru-RU"
                f"&app_name=tiktok_web&browser_language=ru-RU"
                f"&browser_name=Mozilla&browser_platform=Win32"
                f"&browser_version=5.0+(Windows)"
                f"&device_id=000000000000000000"
                f"&device_platform=web_pc"
                f"&itemId={aweme_id}"
                f"&os=windows&region=PL"
                f"&screen_height=0&screen_width=0",
            )
        )["data"]["signed_url"]

        return (await self.engine.get(new_url, encoded=True))["itemInfo"]["itemStruct"]

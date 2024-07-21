import aiohttp
from attrs import define

from bot.utils.config import config

from ..common.engine import CommonEngine
from ..common.exceptions import EndpointNotFound

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
)


@define
class TikTokEngine(CommonEngine):
    async def restart_session(self):
        try:
            await self.session.close()

        except AttributeError:
            pass

        finally:
            self.session = aiohttp.ClientSession(headers={"User-Agent": USER_AGENT})

    async def post(self, url: str, data: str = ""):
        try:
            async with self.session.post(
                url,
                data=data,
            ) as r:
                if r.status != 200:
                    raise EndpointNotFound(r.url)
                if config.log.log_endpoints:
                    print(r.url)

                return await r.json()

        except AttributeError:
            await self.restart_session()
            return await self.post(url, data)

import orjson
from attrs import define

from bot.utils.config import config

from ..common.engine import CommonEngine
from ..common.exceptions import EndpointNotFound


@define
class ContentStudioEngine(CommonEngine):
    async def get(self, url: str, json: dict = None):
        try:
            async with self.session.post(
                url, json=(json or {}), headers={"Content-Type": "application/json"}
            ) as r:
                if r.status != 200:
                    raise EndpointNotFound(r.url)
                if config.log.log_endpoints:
                    print(r.url)
                return orjson.loads(await r.read())

        except AttributeError:
            await self.restart_session()
            return await self.get(url, json)

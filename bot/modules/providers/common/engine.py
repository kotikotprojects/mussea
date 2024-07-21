import aiohttp
from attrs import define
from yarl import URL

from bot.utils.config import config

from .exceptions import EndpointNotFound, TooBig


@define
class CommonEngine:
    session: aiohttp.ClientSession = None

    async def restart_session(self):
        try:
            await self.session.close()
        except AttributeError:
            pass
        finally:
            self.session = aiohttp.ClientSession()

    async def close_session(self):
        try:
            await self.session.close()

        except AttributeError:
            pass

    async def __read_without_content_length(self, url, params, limit):
        async with self.session.get(
            url,
            params=(params or {}),
        ) as r:
            if r.status != 200:
                raise EndpointNotFound(r.url)
            content = bytearray()
            async for chunk in r.content.iter_chunked(1024 * 1024):
                # noinspection PyTypeChecker
                content.extend(chunk)
                if len(content) > limit:
                    raise TooBig(r.url)
            return bytes(content)

    async def read_data(self, url: str, params: dict = None, limit: int = 52428800):
        try:
            async with self.session.get(
                url,
                params=(params or {}),
            ) as r:

                if r.status != 200:
                    raise EndpointNotFound(r.url)
                if r.content_length is None:
                    return await self.__read_without_content_length(url, params, limit)
                if r.content_length > limit:
                    raise TooBig(r.url)

                return await r.read()

        except AttributeError:
            await self.restart_session()
            return await self.read_data(url, params)

    async def get(self, url: str, params: dict = None, encoded: bool = False):
        try:
            async with self.session.get(
                url if not encoded else URL(url, encoded=True),
                params=(params or {}),
            ) as r:
                if r.status != 200:
                    raise EndpointNotFound(r.url)
                if config.log.log_endpoints:
                    print(r.url)

                return await r.json()

        except AttributeError:
            await self.restart_session()
            return await self.get(url, params)

    async def real_url(self, url: str) -> str:
        try:
            async with self.session.head(url, allow_redirects=True) as resp:
                return str(resp.url)

        except AttributeError:
            await self.restart_session()
            return await self.real_url(url)

    async def check_exists(self, url: str):
        try:
            async with self.session.head(url, allow_redirects=True) as resp:
                return resp.status == 200

        except AttributeError:
            await self.restart_session()
            return await self.check_exists(url)

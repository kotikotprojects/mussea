import aiohttp
from attrs import define
from bot.utils.config import config

USER_AGENT = (
    "com.ss.android.ugc.33.3.4/330304 (Linux; U; Android 13; en_US; Pixel 7; "
    "Build/TD1A.220804.031; Cronet/58.0.2991.0)"
)


@define
class TikTokEngine:
    session: aiohttp.ClientSession = None

    async def restart_session(self):
        try:
            await self.session.close()
        except AttributeError:
            pass
        finally:
            self.session = aiohttp.ClientSession(headers={"User-Agent": USER_AGENT})

    async def close_session(self):
        try:
            await self.session.close()
        except AttributeError:
            pass

    async def read_data(self, url: str, params: dict = None, limit: int = 52428800):
        try:
            async with self.session.get(
                url,
                params=(params or {}),
            ) as r:
                if r.status == 200:
                    content = bytearray()
                    async for chunk in r.content.iter_chunked(1024 * 1024):
                        # noinspection PyTypeChecker
                        content.extend(chunk)
                        if len(content) > limit:
                            return None
                    return bytes(content)
                else:
                    return None
        except AttributeError:
            await self.restart_session()
            return await self.read_data(url, params)

    async def get(self, url: str, params: dict = None):
        try:
            async with self.session.get(
                url,
                params=(params or {}),
            ) as r:
                if r.status != 200:
                    raise Exception
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

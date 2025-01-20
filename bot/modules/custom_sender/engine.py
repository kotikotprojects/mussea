import aiohttp
from attrs import define

from bot.utils import env


@define
class BotEngine:
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

    async def get_api(self, method: str, json: dict):
        try:
            async with self.session.post(
                f"https://api.telegram.org/bot{env.BOT_TOKEN}/{method}",
                json=json,
            ) as r:
                return await r.json()

        except AttributeError:
            await self.restart_session()
            return await self.get_api(method, json)

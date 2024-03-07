import aiohttp
from attrs import define

from ..common.engine import CommonEngine

USER_AGENT = (
    "com.ss.android.ugc.33.3.4/330304 (Linux; U; Android 13; en_US; Pixel 7; "
    "Build/TD1A.220804.031; Cronet/58.0.2991.0)"
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

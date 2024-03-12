from attrs import define

from .driver import BotDriver


@define
class Methods:
    driver: BotDriver

    async def send_video(self, url: str, chat_id: int, reply_to_message_id: int):
        return await self.driver.send_video(url, chat_id, reply_to_message_id)

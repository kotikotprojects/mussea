from attrs import define

from .engine import BotEngine


@define
class BotDriver:
    engine: BotEngine

    async def send_video(self, url: str, chat_id: int, reply_to_message_id: int):
        return await self.engine.get_api(
            method="sendVideo",
            json={
                "chat_id": chat_id,
                "video": url,
                "reply_parameters": {"message_id": reply_to_message_id},
            },
        )

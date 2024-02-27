from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, ReactionTypeEmoji


class LikeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        res = await handler(event, data)
        await event.react(reaction=[ReactionTypeEmoji(emoji="❤")])
        return res

from aiogram import Bot
from aiogram.dispatcher import router as s_router
from aiogram.types.error_event import ErrorEvent
from rich.traceback import Traceback

from bot.common import console


async def on_error(event: ErrorEvent, bot: Bot):
    import base64
    import os

    error_id = base64.urlsafe_b64encode(os.urandom(6)).decode()

    traceback = Traceback.from_exception(
        type(event.exception),
        event.exception,
        event.exception.__traceback__,
        show_locals=True,
        suppress=[s_router],
    )

    if event.update.chosen_inline_result:
        await bot.edit_message_caption(
            inline_message_id=event.update.chosen_inline_result.inline_message_id,
            caption=f"💔 <b>ERROR</b> occurred. Use this code to search in logs: "
            f"<code>{error_id}</code>",
            parse_mode="HTML",
        )

    if event.update.message:
        await event.update.message.reply(
            text=f"💔 <b>ERROR</b> occurred. Use this code to search in logs: "
            f"<code>{error_id}</code>",
            parse_mode="HTML",
        )

    console.print(f"[red]{error_id} occurred[/]")
    console.print(event)
    console.print(traceback)
    console.print(f"-{error_id} occurred-")

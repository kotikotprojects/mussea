from aiogram import Bot, Router
from rich import print

router = Router()


@router.startup()
async def startup(bot: Bot):
    print(f"[green]Started as[/] @{(await bot.me()).username}")


@router.shutdown()
async def shutdown():
    from bot.modules.custom_sender import custom_sender
    from bot.modules.providers.contentstudio import contentstudio
    from bot.modules.providers.tiktokapi import tiktokapi

    await tiktokapi.engine.close_session()
    await contentstudio.engine.close_session()
    await custom_sender.engine.close_session()

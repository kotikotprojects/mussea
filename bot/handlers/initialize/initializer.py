from aiogram import Bot, Router
from rich import print

router = Router()


@router.startup()
async def startup(bot: Bot):
    print(f"[green]Started as[/] @{(await bot.me()).username}")


@router.shutdown()
async def shutdown():
    from bot.modules.tiktok import tiktok

    await tiktok.engine.close_session()

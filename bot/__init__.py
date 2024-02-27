import contextlib

from rich import print


async def runner():
    from . import handlers
    from .common import bot, dp
    from .modules.error import on_error

    dp.error.register(on_error)
    dp.include_routers(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def plugins():
    from rich import traceback

    traceback.install(show_locals=True)


def main():
    import asyncio

    plugins()

    print("Starting...")
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(runner())

    print("[red]Stopped.[/]")

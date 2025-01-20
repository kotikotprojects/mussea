from aiogram import Bot, Dispatcher
from rich.console import Console

from .utils import config, env

bot = Bot(token=env.BOT_TOKEN)
dp = Dispatcher()
console = Console()


__all__ = ["bot", "dp", "config", "console"]

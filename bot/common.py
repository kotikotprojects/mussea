from aiogram import Bot, Dispatcher
from rich.console import Console

from .utils.config import config

bot = Bot(token=config.telegram.bot_token)
dp = Dispatcher()
console = Console()


__all__ = ["bot", "dp", "config", "console"]

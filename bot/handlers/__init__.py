from aiogram import Router

from bot.middlewares import LikeMiddleware

from . import initialize, start, tiktok

router = Router()

router.message.middleware(LikeMiddleware())

router.include_routers(initialize.router, start.router, tiktok.router)

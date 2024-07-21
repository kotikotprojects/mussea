from aiogram import Router

from . import initialize, start, tiktok

router = Router()

router.include_routers(initialize.router, start.router, tiktok.router)

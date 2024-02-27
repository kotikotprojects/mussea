from aiogram import Router, types, exceptions

from bot.filters import TikTokUrlFilter
from bot.modules.tiktok import Photos, Video, tiktok
from bot.utils.config import config
from rich import print

router = Router()


@router.message(TikTokUrlFilter())
async def on_tiktok(message: types.Message):
    for url in TikTokUrlFilter.get_tiktoks(message):
        init_msg = await message.reply("🌊 Downloading...")

        if config.log.log_tiktoks:
            print(  # noqa
                f"""\[{f"@{message.from_user.username}" if 
                message.from_user.username else message.from_user.id}] {url}"""
            )

        content = await tiktok.content.from_url(url)
        await init_msg.delete()

        if isinstance(content, Video):
            try:
                await message.reply_video(content.url)
            except exceptions.TelegramBadRequest:
                err_msg = await message.reply(
                    "😨 Telegram cannot download provided video. "
                    "But don't worry! We will fix everything for you in a moment."
                )
                try:
                    await (
                        lambda file: message.reply_video(
                            types.BufferedInputFile(
                                filename="mussea.mp4",
                                file=file,
                            )
                        )
                        if file
                        else message.reply("💔 File is probably too big for us")
                    )(file=await tiktok.engine.read_data(content.url))
                    await err_msg.delete()
                except exceptions.TelegramBadRequest:
                    await err_msg.edit_text("💔 Telegram didn't accept even our file")

        elif isinstance(content, Photos):
            chunk_start = 0
            while chunk_start < len(content.urls):
                chunk_end = min(chunk_start + 10, len(content.urls))
                if chunk_end - chunk_start == 1 and len(content.urls) > 2:
                    chunk_end -= 1

                current_chunk = content.urls[chunk_start:chunk_end]

                if len(current_chunk) > 1:
                    await message.reply_media_group(
                        [types.InputMediaPhoto(media=url) for url in current_chunk]
                    )
                else:
                    await message.reply_photo(current_chunk[0])

                chunk_start = chunk_end

            if content.audio_url:
                await message.reply_audio(
                    audio=content.audio_url,
                    title=content.audio_title,
                    performer=content.audio_author,
                )

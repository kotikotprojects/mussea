from aiogram import Router, types
from rich import print
from rich.traceback import Traceback

from bot.filters import TikTokUrlFilter
from bot.modules.custom_sender import custom_sender
from bot.modules.cycle.cycle import LinkCycle
from bot.modules.cycle.estimator import process_situation
from bot.utils.config import config

router = Router()


@router.message(TikTokUrlFilter())
async def on_tiktok(message: types.Message):
    for url in TikTokUrlFilter.get_tiktoks(message):
        if config.log.log_tiktoks:
            print(  # noqa
                f"""\[{f"@{message.from_user.username}" if 
                message.from_user.username else message.from_user.id}] {url}"""
            )
        init_msg = await message.reply("🌊 Downloading...")
        cycle = LinkCycle(url).set_estimate()
        while not cycle.finished:
            cycle = await process_situation(cycle)

            if cycle.end_error:
                await message.reply(
                    text="💔 Cannot download your video. None of our providers could process this request. "
                         "Maybe the video doesn't exist or TikTok servers are shut down?"
                )
                cycle.set_finished()

            if not cycle.job.send:
                continue

            try:
                if cycle.video:
                    if not (
                        await custom_sender.methods.send_video(
                            url=cycle.video.url,
                            chat_id=message.chat.id,
                            reply_to_message_id=message.message_id,
                        )
                    ).get("ok"):
                        await message.reply_video(
                            video=types.URLInputFile(url=cycle.video.url)
                        )
                if cycle.photos:
                    for chunk in cycle.photos.urls_chunked:
                        if len(chunk) > 1:
                            await message.reply_media_group(
                                [types.InputMediaPhoto(media=url) for url in chunk]
                            )
                        else:
                            await message.reply_photo(chunk[0])
                if cycle.audio:
                    await message.reply_audio(audio=cycle.audio)

                cycle.set_finished()

            except Exception as e:
                assert e
                if config.log.log_cycle_errors:
                    print("ERROR IN CYCLE")
                    print(Traceback(show_locals=True))
                    print("END ERROR IN CYCLE")
                cycle.set_estimate()

        await init_msg.delete()

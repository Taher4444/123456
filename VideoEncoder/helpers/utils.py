#  Copyright (C) 2021 The Authors

from os import remove
from VideoEncoder import data, download_dir
from .ffmpeg_utils import encode, get_thumbnail, get_duration, get_width_height
from telethon.tl.types import DocumentAttributeVideo
from .. import download_dir


async def on_task_complete():
    del data[0]
    if len(data) > 0:
        await add_task(data[0])


async def add_task(event):
    try:
        msg = await event.reply("🟡 Downloading video...🟡\n\n⚙️Engine: Telethon\n\n#downloading`")
        filepath = await event.download_media(download_dir)
        await msg.edit("`🟣 Encoding video... 🟣\n\n⚙️Engine: FFMPEG\n\n#encoding`")
        new_file = encode(filepath)
        if new_file:
            await msg.edit("`🔵 Getting metadata...🔵`")
            duration = get_duration(new_file)
            thumb = get_thumbnail(new_file, download_dir, duration / 4)
            width, height = get_width_height(new_file)
            await msg.edit("`⚪ Uploading video...⚪\n\n⚙️ Engine: Pyrogram\n\n#uploading`")
            await event.client.send_file(
                event.chat_id,
                file=new_file,
                supports_streaming=True,
                thumb=thumb,
                attributes=[
                    DocumentAttributeVideo(duration=duration, w=width, h=height)
                ],
            )
            remove(new_file)
            remove(thumb)
            await msg.edit("`🟢 Video Encoded 🟢\n\n#encoded`")
        else:
            await msg.edit(
                "`🔴 Something wents wrong while encoding your file.`"
            )
            remove(filepath)
    except Exception as e:
        await msg.edit(f"**🔴 ERROR 🔴**:\n\n`{e}\n\n#error`")
    await on_task_complete()

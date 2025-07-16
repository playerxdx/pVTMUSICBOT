# plugins/play.py

import os
from telethon import events
from config import OWNER_ID
from core.vc import join_and_stream


def register(clients):
    bot = clients.bot

    @bot.on(events.NewMessage(pattern="/(vplay|splay)"))
    async def _(event):
        if event.sender_id != OWNER_ID:
            return await event.reply("🚫 You're not allowed to use this bot.")

        if not event.is_reply:
            return await event.reply("⚠️ Reply to an audio or video file to play it in voice chat.")

        reply = await event.get_reply_message()
        if not reply.file or not reply.media:
            return await event.reply("❌ That’s not a valid audio/video file.")

        media = await reply.download_media(file="downloads/")
        chat_id = event.chat_id
        await event.reply(f"▶️ Streaming `{os.path.basename(media)}` ...")
        await join_and_stream(clients, chat_id, media)

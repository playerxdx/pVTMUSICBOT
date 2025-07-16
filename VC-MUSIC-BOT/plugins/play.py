# plugins/play.py

from telethon import events
from config import SUDO_USERS, OWNER_ID
from utils.clients import user, bot, vc
import os

# Buttons: if you still want inline controls, you can define them via Telegram Bot API Style here.

@bot.on(events.NewMessage(pattern="/vplay"))
async def play_handler(event):
    sender = event.sender_id
    if sender not in SUDO_USERS and sender != OWNER_ID:
        return await event.reply("❌ You're not authorized to use this command.")

    if not event.is_reply:
        return await event.reply("❗ Reply to an audio/video file to play it in VC.")

    reply = await event.get_reply_message()
    if not reply.media:
        return await event.reply("❗ That message doesn't contain a media file.")

    media_path = await reply.download_media(file="downloads/")
    if not os.path.exists(media_path):
        return await event.reply("⚠️ Failed to download the media file.")

    # Join voice chat and stream
    await vc.join_group_call(event.chat_id, InputAudioStream(media_path))
    await event.reply(f"▶️ Streaming started: {os.path.basename(media_path)}\nRequested by: [{event.sender.first_name}](tg://user?id={sender})")

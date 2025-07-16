from telethon import events
from config import SUDO_USERS, OWNER_ID
from utils.clients import vc, bot
from pytgcalls.types.input_stream import InputAudioStream
import os

@bot.on(events.NewMessage(pattern="/vplay"))
async def play_handler(event):
    if event.sender_id not in SUDO_USERS and event.sender_id != OWNER_ID:
        return await event.reply("You're not authorized.")

    if not event.is_reply:
        return await event.reply("Reply to a file to play in VC.")

    reply = await event.get_reply_message()
    media = await reply.download_media(file="downloads/")
    if not os.path.exists(media):
        return await event.reply("Failed to download media.")

    await vc.join_group_call(
        event.chat_id,
        InputAudioStream(media)
    )

    await event.reply("▶️ **Streaming started!**")

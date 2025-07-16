from telethon import events
from config import SUDO_USERS, OWNER_ID
from utils.clients import user, bot, vc
from core.vc import join_and_stream
from pytgcalls.types.input_stream import InputAudioStream
from utils.buttons import get_control_buttons
import os

@bot.on(events.NewMessage(pattern="/vplay"))
async def play_handler(event):
    if event.sender_id not in SUDO_USERS and event.sender_id != OWNER_ID:
        return await event.reply("You're not authorized to use this command.")

    if not event.is_reply:
        return await event.reply("Reply to an audio or video file to play it in VC.")

    reply = await event.get_reply_message()
    if not reply.file:
        return await event.reply("This message doesn't contain a media file.")

    media = await reply.download_media(file="downloads/")
    if not os.path.exists(media):
        return await event.reply("Failed to download media.")

    chat_id = event.chat_id

    await join_and_stream(
        clients=vc,
        chat_id=chat_id,
        file_path=media
    )

    await event.reply(
        f"▶️ **Started Streaming!**\n\n**Requested by:** [{event.sender.first_name}](tg://user?id={event.sender_id})",
        buttons=get_control_buttons()
    )

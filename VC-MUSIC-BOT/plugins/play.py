from telethon import events
from config import SUDO_USERS, OWNER_ID
from utils.clients import vc, bot
from pytgcalls.types.input_stream import AudioPiped  # ✅ Compatible stream class
from utils.buttons import get_control_buttons
from plugins import seek
import os

@bot.on(events.NewMessage(pattern="/vplay"))
async def play_handler(event):
    if event.sender_id not in SUDO_USERS and event.sender_id != OWNER_ID:
        return await event.reply("❌ You're not authorized to use this command.")

    if not event.is_reply:
        return await event.reply("ℹ️ Reply to an audio or video file to play it in VC.")

    reply = await event.get_reply_message()
    if not reply.file:
        return await event.reply("❌ This message doesn't contain a media file.")

    media = await reply.download_media(file="downloads/")
    if not os.path.exists(media):
        return await event.reply("⚠️ Failed to download media.")

    chat_id = event.chat_id

    try:
        await vc.join_group_call(
            chat_id,
            AudioPiped(media),  # ✅ Correct stream for pytgcalls 0.9.7
            stream_type="local_stream",  # optional but safe
        )

        seek.set_playing(chat_id, media)

        await event.reply(
            "▶️ **Started Streaming!**",
            buttons=get_control_buttons()
        )
    except Exception as e:
        await event.reply(f"❌ Error: `{str(e)}`")

def register(clients):
    # Nothing needed if handlers are declared globally
    pass

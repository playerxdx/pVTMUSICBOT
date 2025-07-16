from telethon import events
from config import OWNER_ID, SUDO_USERS
from utils.clients import bot, vc
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
import os

# Dictionary to track current file for each VC chat
playing_chat = {}

@bot.on(events.NewMessage(pattern="/seek"))
async def seek_handler(event):
    if event.sender_id != OWNER_ID and event.sender_id not in SUDO_USERS:
        return await event.reply("You're not allowed to use this command.")

    args = event.raw_text.split()
    if len(args) < 2 or not args[1].isdigit():
        return await event.reply("Usage: `/seek <seconds>`", parse_mode="md")

    chat_id = event.chat_id
    seconds = int(args[1])

    if chat_id not in playing_chat:
        return await event.reply("Nothing is streaming in this chat.")

    file_path = playing_chat[chat_id]

    if not os.path.exists(file_path):
        return await event.reply("The file being streamed is missing.")

    # Restart the stream from new position
    await vc.leave_group_call(chat_id)
    await vc.join_group_call(

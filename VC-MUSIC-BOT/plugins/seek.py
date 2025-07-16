# plugins/seek.py

from telethon import events
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types import Update
from pytgcalls.types.stream.quality import HighQualityAudio
from utils.clients import bot, vc
from config import OWNER_ID, SUDO_USERS
import os

active_chats = {}  # To track file paths per chat

@bot.on(events.NewMessage(pattern="/seek"))
async def seek_handler(event):
    if event.sender_id not in SUDO_USERS and event.sender_id != OWNER_ID:
        return await event.reply("You're not authorized to use this command.")

    chat_id = event.chat_id
    if chat_id not in active_chats:
        return await event.reply("No active stream in this chat.")

    try:
        seconds = int(event.raw_text.split(maxsplit=1)[1])
    except (IndexError, ValueError):
        return await event.reply("Usage: `/seek <seconds>`")

    file_path = active_chats[chat_id]
    if not os.path.exists(file_path):
        return await event.reply("File not found.")

    await vc.leave_group_call(chat_id)
    await vc.join_group_call(
        chat_id,
        InputAudioStream(
            file_path,
            duration=None,
            offset=seconds * 1000  # offset is in milliseconds
        ),
        stream_type=HighQualityAudio()
    )

    await event.reply(f"⏩ Seeked forward by `{seconds}` seconds.")

@bot.on(events.NewMessage(pattern="/seekback"))
async def seekback_handler(event):
    if event.sender_id not in SUDO_USERS and event.sender_id != OWNER_ID:
        return await event.reply("You're not authorized to use this command.")

    chat_id = event.chat_id
    if chat_id not in active_chats:
        return await event.reply("No active stream in this chat.")

    try:
        seconds = int(event.raw_text.split(maxsplit=1)[1])
    except (IndexError, ValueError):
        return await event.reply("Usage: `/seekback <seconds>`")

    file_path = active_chats[chat_id]
    if not os.path.exists(file_path):
        return await event.reply("File not found.")

    await vc.leave_group_call(chat_id)
    await vc.join_group_call(
        chat_id,
        InputAudioStream(
            file_path,
            duration=None,
            offset=-seconds * 1000  # Negative offset to rewind
        ),
        stream_type=HighQualityAudio()
    )

    await event.reply(f"⏪ Seeked backward by `{seconds}` seconds.")

def set_active_file(chat_id: int, file_path: str):
    active_chats[chat_id] = file_path

def clear_active_file(chat_id: int):
    if chat_id in active_chats:
        del active_chats[chat_id]

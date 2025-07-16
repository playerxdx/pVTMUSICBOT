# plugins/seek.py

from telethon import events
from telethon.tl.types import Message
from config import OWNER_ID
from utils.clients import vc
from pytgcalls.types.input_stream import InputAudioStream
import os
import asyncio

# Dictionary to store file path for each chat
playing_files = {}

def register(clients):
    bot = clients.bot

    @bot.on(events.NewMessage(pattern="/seek"))
    async def seek_forward_handler(event: Message):
        if event.sender_id != OWNER_ID:
            return await event.reply("❌ You're not allowed to use this command.")

        chat_id = event.chat_id
        seconds = 10  # seek forward by 10 seconds

        if chat_id not in playing_files:
            return await event.reply("❗ No file is playing in this chat.")

        file_path = playing_files[chat_id]
        if not os.path.exists(file_path):
            return await event.reply("❌ File not found.")

        await vc.leave_group_call(chat_id)
        await asyncio.sleep(1)

        await vc.join_group_call(
            chat_id,
            InputAudioStream(
                file_path,
                duration=None,
                offset=seconds * 1000  # offset in ms
            )
        )
        await event.reply("⏩ Seeked forward by 10 seconds!")

    @bot.on(events.NewMessage(pattern="/seekback"))
    async def seek_back_handler(event: Message):
        if event.sender_id != OWNER_ID:
            return await event.reply("❌ You're not allowed to use this command.")

        chat_id = event.chat_id
        seconds = -10  # seek backward by 10 seconds

        if chat_id not in playing_files:
            return await event.reply("❗ No file is playing in this chat.")

        file_path = playing_files[chat_id]
        if not os.path.exists(file_path):
            return await event.reply("❌ File not found.")

        await vc.leave_group_call(chat_id)
        await asyncio.sleep(1)

        await vc.join_group_call(
            chat_id,
            InputAudioStream(
                file_path,
                duration=None,
                offset=max(0, seconds * 1000)
            )
        )
        await event.reply("⏪ Seeked backward by 10 seconds!")

    # This should be called from play.py after starting a stream
    def set_playing(chat_id, file_path):
        playing_files[chat_id] = file_path

    # Export function for setting track from other modules
    return {"set_playing": set_playing}

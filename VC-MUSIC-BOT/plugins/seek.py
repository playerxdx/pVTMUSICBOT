# plugins/seek.py

import os
import asyncio
from telethon import events, Button
from config import OWNER_ID
from core.vc import join_and_stream

# Seconds to seek
SEEK_STEP = 10  # adjust as needed

# Store last file & seek info per chat
last_playback = {}

def register(clients):
    bot = clients.bot

    @bot.on(events.CallbackQuery())
    async def callback_handler(event):
        if event.sender_id != OWNER_ID:
            return await event.answer("Not allowed!", alert=True)

        data = event.data.decode("utf-8")
        chat_id = event.chat_id

        if chat_id not in last_playback:
            return await event.answer("Nothing to seek.", alert=True)

        file_path = last_playback[chat_id]["file"]
        position = last_playback[chat_id]["seek"]

        if data == "seek":
            position += SEEK_STEP
        elif data == "seekback":
            position = max(0, position - SEEK_STEP)

        # Restart stream from new position
        await join_and_stream(clients, chat_id, file_path + f"?ss={position}")
        last_playback[chat_id]["seek"] = position

        await event.answer(f"⏩ Moved to {position}s", alert=True)

    # Hook into play command to track file
    def save_playback(chat_id, file):
        last_playback[chat_id] = {
            "file": file,
            "seek": 0
        }

    # expose hook
    clients.seek_hook = save_playback

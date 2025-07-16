# plugins/seek.py
# plugins/seek.py

from telethon import events
from config import SUDO_USERS, OWNER_ID
from utils.clients import vc
from utils.stream_helpers import restart_stream_from_position  # if you have this helper


SEEK_STEP = 10
last_playback = {}

def register(clients):
    bot = clients.bot
    vc = clients.vc

    @bot.on(events.CallbackQuery())
    async def callback_handler(event):
        if event.sender_id != OWNER_ID:
            return await event.answer("🚫 Not allowed", alert=True)

        data = event.data.decode("utf-8")
        chat_id = event.chat_id

        if data in ["pause", "resume", "close"]:
            if data == "pause":
                await vc.pause_stream(chat_id)
                return await event.answer("⏸ Paused", alert=True)
            if data == "resume":
                await vc.resume_stream(chat_id)
                return await event.answer("🔁 Resumed", alert=True)
            if data == "close":
                await leave_vc(clients, chat_id)
                return await event.edit("❌ Playback stopped. VC left.")

        if chat_id not in last_playback:
            return await event.answer("No active playback", alert=True)

        file_path = last_playback[chat_id]["file"]
        position = last_playback[chat_id]["seek"]

        if data == "seek":
            position += SEEK_STEP
        elif data == "seekback":
            position = max(0, position - SEEK_STEP)

        await join_and_stream(clients, chat_id, file_path + f"?ss={position}")
        last_playback[chat_id]["seek"] = position
        await event.answer(f"⏩ Moved to {position}s", alert=True)

    def save_playback(chat_id, file):
        last_playback[chat_id] = {
            "file": file,
            "seek": 0
        }

    clients.seek_hook = save_playback

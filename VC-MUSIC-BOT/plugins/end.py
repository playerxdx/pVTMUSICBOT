# plugins/end.py

from telethon import events
from config import OWNER_ID
from core.vc import leave_vc

def register(clients):
    bot = clients.bot

    @bot.on(events.NewMessage(pattern="/end"))
    async def _(event):
        if event.sender_id != OWNER_ID:
            return await event.reply("🚫 You're not allowed to use this command.")

        chat_id = event.chat_id
        await leave_vc(clients, chat_id)
        await event.reply("⏹️ Playback ended. Left voice chat.")

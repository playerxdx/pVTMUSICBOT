# plugins/end.py

from telethon import events
from config import OWNER_ID, SUDO_USERS
from utils.clients import vc

def register(clients):
    bot = clients.bot

    @bot.on(events.NewMessage(pattern="/end"))
    async def end_handler(event):
        if event.sender_id not in SUDO_USERS and event.sender_id != OWNER_ID:
            return await event.reply("❌ You're not authorized to use this command.")

        try:
            await vc.leave_group_call(event.chat_id)
            await event.reply("⏹️ **Stopped streaming and left the VC.**")
        except Exception as e:
            await event.reply(f"❌ Failed to leave VC:\n`{e}`")

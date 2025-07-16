# plugins/start_help.py

from telethon import events, Button
from config import OWNER_ID

def register(clients):
    bot = clients.bot

    async def start_handler(event):
        if event.sender_id != OWNER_ID:
            return await event.reply("👋 Hello! This is a private VC music bot.")

        await event.reply(
            "**✨ Welcome to Pvt VC Music Bot!**\n\n"
            "Control music with inline buttons, stream any audio/video file in voice chat.\n"
            "Only the owner can use commands.\n\n"
            "💡 Click the Help button below for more info.",
            buttons=[[Button.inline("📜 Help", data="show_help")]]
        )

    @bot.on(events.NewMessage(pattern="/start"))
    async def start_command(event):
        await start_handler(event)

    @bot.on(events.CallbackQuery(data=b"show_help"))
    async def show_help(event):
        if event.sender_id != OWNER_ID:
            return await event.answer("Access denied.", alert=True)

        await event.edit(
            "**📝 Command List:**\n\n"
            "🎵 `/vplay` - Reply to video to play in VC\n"
            "🎵 `/splay` - Reply to audio file to play in VC\n"
            "⏹ `/end` - Stop and leave VC\n\n"
            "**Inline Controls:**\n"
            "⏪ SeekBack | ⏩ Seek\n"
            "⏸ Pause | 🔁 Resume | ❌ Close",
            buttons=[[Button.inline("🔙 Back", data="start_menu")]]
        )

    @bot.on(events.CallbackQuery(data=b"start_menu"))
    async def back_to_start(event):
        await start_handler(event)

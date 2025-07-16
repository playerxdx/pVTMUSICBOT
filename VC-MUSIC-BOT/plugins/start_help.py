from telethon import events
from config import OWNER_ID

@events.register(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply(f"👋 Welcome to the VC Music Bot!\n\nOwner: [{OWNER_ID}](tg://user?id={OWNER_ID})")

@events.register(events.NewMessage(pattern="/help"))
async def help_cmd(event):
    await event.reply("🎵 Available Commands:\n\n/vplay - Play replied video/audio\n/splay - Play in stream mode\n/end - End VC\n/seek - Forward\n/seekback - Backward")

# bot.py

import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from pytgcalls import GroupCallFactory # Not py_tgcalls
from config import API_ID, API_HASH, BOT_TOKEN, SESSION
from plugins import play, end, seek, start_help

assistant = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
# Bot account (used for handling bot commands)
bot = TelegramClient(StringSession(SESSION), API_ID, API_HASH).start()

# VC streaming client
vc_client = PyTgCalls(assistant)

# Store clients for plugin use
class Clients:
    bot = bot
    assistant = assistant
    vc = vc_client

clients = Clients()

# Register all command handlers
play.register(clients)
end.register(clients)
seek.register(clients)
start_help.register(clients)

async def main():
    print("Starting assistant...")
    await assistant.start()
    await vc_client.start()
    print("Bot is up. Assistant joined. VC streaming ready.")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())

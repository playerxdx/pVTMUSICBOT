import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN, SESSION

# Start the assistant (user) client using StringSession
user = TelegramClient(StringSession(SESSION), API_ID, API_HASH).start()

# Start the bot client using bot token
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Initialize PyTgCalls with the user (assistant) client
vc = PyTgCalls(user)

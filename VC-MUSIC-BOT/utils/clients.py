import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION

# Initialize assistant client (user account)
user = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
user.start()

# Initialize bot client (bot account)
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Voice chat client
vc = PyTgCalls(user)

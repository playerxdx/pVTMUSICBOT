import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SESSION


# Initialize assistant client (user account)
user = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
user.start()

# Initialize bot client (bot account)
bot = TelegramClient(StringSession(SESSION), API_ID, API_HASH).start()

# Voice chat client
vc = PyTgCalls(user)

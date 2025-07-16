from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH, STRING_SESSION

with TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH) as client:
    me = client.get_me()
    print(f"✅ Logged in as {me.first_name} (ID: {me.id})")

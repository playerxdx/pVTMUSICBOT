from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("\n✅ Your new STRING_SESSION:\n")
    print(client.session.save())

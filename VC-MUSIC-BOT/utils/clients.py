import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from pytgcalls import GroupCallFactory
from config import API_ID, API_HASH, BOT_TOKEN, SESSION

user = TelegramClient(StringSession(SESSION), API_ID, API_HASH).start()
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
vc = GroupCallFactory(user).get_file_group_call()


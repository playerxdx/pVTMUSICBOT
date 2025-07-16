from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, STRING_SESSION

bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=os.environ.get("BOT_TOKEN"))
user = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
vc = PyTgCalls(user)

class Clients:
    def __init__(self):
        self.bot = bot
        self.assistant = user
        self.vc = vc

vc = Clients()

# plugins/seek.py

from telethon import events
from config import SUDO_USERS, OWNER_ID
from utils.clients import vc
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
import os

playing_chat = {}  # You should store this globally somewhere if persistent

@vc.on_stream_end()
async def stream_ended_handler(_, update):
    chat_id = update.chat_id
    if chat_id in playing_chat:
        del playing_chat[chat_id]

@vc.client.on(events.NewMessage(pattern="/seek"))
async def seek_handler(event):
    if event.sender_id not in SUDO_USERS and event.sender_id != OWNER_ID:
        return await event.reply("❌ You're not authorized to use this command.")
    
    chat_id = event.chat_id
    if chat_id not in playing_chat:
        return await event.reply("❗ Nothing is playing to seek.")
    
    try:
        seconds = int(event.text.split(maxsplit=1)[1])
    except:
        return await event.reply("⚠️ Usage: `/seek 30` to seek forward 30 seconds.")

    current_file = playing_chat[chat_id]
    
    await vc.leave_group_call(chat_id)
    await vc.join_group_call(
        chat_id,
        InputAudioStream(
            current_file,
            duration_kb=0,
            initial_seek=seconds * 1000,
            audio_parameters=HighQualityAudio()
        )
    )

    await event.reply(f"⏩ Seeked forward {seconds} seconds.")

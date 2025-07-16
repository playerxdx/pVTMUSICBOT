# plugins/play.py

from pyrogram.types import Message
from telethon.tl.functions.phone import CreateGroupCallRequest
from telethon.tl.functions.phone import DiscardGroupCallRequest
from telethon.tl.types import InputGroupCall
from telethon.tl.functions.phone import GetGroupCallRequest
from telethon.errors import UserAlreadyParticipantError

from utils.clients import user, bot, vc
from config import OWNER_ID
from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.input_audio_stream import InputAudioStream

import os
import asyncio
import aiofiles

active_chats = {}

BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("⏸ Pause", callback_data="pause"),
        InlineKeyboardButton("▶️ Resume", callback_data="resume")
    ],
    [
        InlineKeyboardButton("⏩ Seek", callback_data="seek"),
        InlineKeyboardButton("⏪ Back", callback_data="seekback")
    ],
    [
        InlineKeyboardButton("⏹ Stop", callback_data="end")
    ]
])

@bot.on_message(filters.command("vplay") & filters.user(OWNER_ID))
async def vplay(_, message: Message):
    if message.reply_to_message and message.reply_to_message.audio or message.reply_to_message.video:
        media = message.reply_to_message
    else:
        await message.reply("Reply to a supported audio/video file.")
        return

    file_path = await media.download()
    await user.send_chat_action(message.chat.id, ChatAction.RECORD_AUDIO)

    await vc.join_group_call(
        message.chat.id,
        AudioPiped(file_path)
    )

    active_chats[message.chat.id] = file_path

    await message.reply(
        f"🎧 Playing **{media.audio.title if media.audio else 'file'}** in VC",
        reply_markup=BUTTONS
    )

@bot.on_callback_query()
async def callbacks(_, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data == "pause":
        await vc.pause_stream(chat_id)
        await callback_query.answer("Paused ⏸")

    elif data == "resume":
        await vc.resume_stream(chat_id)
        await callback_query.answer("Resumed ▶️")

    elif data == "seek":
        await callback_query.answer("Seek not implemented")  # Implement later

    elif data == "seekback":
        await callback_query.answer("Seekback not implemented")  # Implement later

    elif data == "end":
        await vc.leave_group_call(chat_id)
        if chat_id in active_chats:
            try:
                os.remove(active_chats[chat_id])
            except Exception:
                pass
            del active_chats[chat_id]
        await callback_query.answer("Stopped ⏹")

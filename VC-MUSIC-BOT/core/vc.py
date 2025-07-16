# core/vc.py

import os
import asyncio
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputStream, AudioPiped
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.exceptions import GroupCallNotFoundError
from telethon.tl.functions.phone import CreateGroupCallRequest, GetGroupCallRequest, DiscardGroupCallRequest
from telethon.tl.types import InputGroupCall, PeerChat

# Join VC and stream a file
async def join_and_stream(clients, chat_id, file_path):
    assistant = clients.assistant
    vc = clients.vc

    # Ensure assistant is in the group
    try:
        await assistant(JoinGroupCall(chat_id))
    except:
        pass  # already in

    try:
        await assistant(GetGroupCallRequest(peer=chat_id))
    except GroupCallNotFoundError:
        await assistant(CreateGroupCallRequest(
            peer=chat_id if isinstance(chat_id, PeerChat) else await assistant.get_input_entity(chat_id),
            random_id=0
        ))

    await vc.join_group_call(
        chat_id,
        InputStream(
            AudioPiped(file_path)
        )
    )

# Stop streaming
async def leave_vc(clients, chat_id):
    await clients.vc.leave_group_call(chat_id)
    try:
        await clients.assistant(DiscardGroupCallRequest(peer=chat_id))
    except:
        pass

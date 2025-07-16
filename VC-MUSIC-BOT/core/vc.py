from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream
from telethon.tl.functions.phone import (
    CreateGroupCallRequest,
    DiscardGroupCallRequest,
    GetGroupCallRequest
)
from telethon.tl.types import PeerChat
from pytgcalls.exceptions import GroupCallNotFoundError


async def join_and_stream(clients, chat_id, file_path):
    assistant = clients.assistant
    vc = clients.vc

    try:
        await assistant(GetGroupCallRequest(peer=chat_id))
    except GroupCallNotFoundError:
        await assistant(CreateGroupCallRequest(
            peer=chat_id if isinstance(chat_id, PeerChat) else await assistant.get_input_entity(chat_id),
            random_id=0
        ))

    a

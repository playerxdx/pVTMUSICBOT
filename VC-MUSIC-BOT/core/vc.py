from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.exceptions import GroupCallNotFoundError
from telethon.tl.functions.phone import (
    CreateGroupCallRequest,
    DiscardGroupCallRequest,
    GetGroupCallRequest
)
from telethon.tl.types import PeerChat

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

    await vc.join_group_call(
        chat_id,
        AudioPiped(file_path)
    )

async def leave_vc(clients, chat_id):
    await clients.vc.leave_group_call(chat_id)
    try:
        await clients.assistant(DiscardGroupCallRequest(peer=chat_id))
    except:
        pass

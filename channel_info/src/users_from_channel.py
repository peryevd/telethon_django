from telethon import functions
from telethon.tl.types import ChannelParticipantsSearch

def getUsersFromChannel(client, channel_name, limit, offset):
    result = client(functions.channels.GetParticipantsRequest(
        channel = channel_name,
        filter = ChannelParticipantsSearch(''),
        offset = offset,
        limit = limit,
        hash = 0
    ))
    
    return result
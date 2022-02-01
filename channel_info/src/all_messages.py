from telethon.tl.functions.messages import GetHistoryRequest

import json

def get_all_messages(client, channel_name, count_limit = 0):
    offset_msg = 0
    limit_msg = 100

    all_messages = []
    total_messages = 0
    total_count_limit = count_limit

    while True:
        history = client(GetHistoryRequest(
            peer=channel_name,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages

        for message in messages:
            all_messages.append(json.loads(message.to_json()))

        offset_msg = messages[len(messages) - 1].id

        total_messages = len(all_messages)

        print("Загружено ", total_messages, "сообщений")

        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    return all_messages
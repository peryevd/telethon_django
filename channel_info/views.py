from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from .serializers import ChannelInfoSerializer, ArticleSerializer

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, InputPhoneContact
from telethon.tl.functions.contacts import ResolveUsernameRequest, DeleteContactsRequest

from .models import ChannelInfo, UsersInfo, MessageChannel, MessageReply

from rest_framework.response import Response
from rest_framework.views import APIView
import json

from telethon.sync import TelegramClient, events
from telethon import functions
import asyncio

from channel_info.src.users_from_channel import *
from channel_info.src.all_users_from_reply import *
from channel_info.src.all_messages import *
from channel_info.src.client import *

from rest_framework.decorators import api_view

from asgiref.sync import sync_to_async

class ChannelInfoListView(ListView):
    model = ChannelInfo
    template_name = 'home.html'

class ChannelDetailView(DetailView): 
    model = ChannelInfo
    template_name = 'channel_detail.html'

class BaseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return self.model.objects.all()

class ChannelInfoViewset(BaseViewSet):
    serializer_class = ChannelInfoSerializer
    model = ChannelInfo

# olsior
# AlexxIT_SmartHome
# rbc_news
# obshchenieo
# TelegramTips

@api_view(['POST'])
def SubNewMes(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
        
    with TelegramClient(username, api_id, api_hash) as client:
        print("Начало прослушивания")
        @client.on(events.NewMessage(chats = request.data['channel_name']))
        async def main(event):
            messages = await sync_to_async(MessageChannel.objects.get, thread_sensitive=True)(id=21)
            messages.json = json.loads(event.to_json())
            await sync_to_async(messages.save, thread_sensitive=True)()
            print(event.message.to_dict()['message'])

        client.run_until_disconnected()
        print("Конец прослушивания")

        return Response({"DONE!"})

@api_view(['POST'])
def GetChannelInfo(request):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with TelegramClient(username, api_id, api_hash) as client:

        # save channel info
        print("Получение информации о канале...")
        result = client(functions.channels.GetFullChannelRequest(channel = request.data['channel_name']))
        ChannelInfo.objects.create(json = json.loads(result.to_json()))
        print("Успешно сохранено!")

        # save users info
        if (result.full_chat.can_view_participants):
            print("Данные о пользователях открыты, загрузка...")
            UsersInfo.objects.create(json = json.loads(getUsersFromChannel(client, request.data['channel_name'], 300, 0).to_json()))
            print("Пользователи успешно сохранены")
        else:
            print("Данные о пользователях закрыты")
            try: 
                if result.chats[1]:
                    print("Найдены комментарии, загрузка...")
                    UsersInfo.objects.create(json = get_all_users_from_reply(client, request.data['channel_name'], 300))
                    print("Комментаторы успешно сохранены")
            except:
                print("Комментарии не найдены, невозможно получить информацию о пользователях")

        #save messages from channel
        print("Получение сообщений канала...")
        MessageChannel.objects.create(json = get_all_messages(client, request.data['channel_name'], 300))
        print("Успешно сохранено!")

        #save messages from reply
        try: 
            if result.chats[1]:
                print("Найдены комментарии, загрузка...")
                MessageReply.objects.create(json = get_all_messages(client, result.chats[1].id, 300))
                print("Сообщения успешно сохранены")
        except:
                print("Комментарии не найдены, невозможно загрузить")

    return Response({"ChannelInfo " + request.data['channel_name'] + " DONE!"})

@api_view(['POST'])
def GetPercent(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with TelegramClient(username, api_id, api_hash) as client:
        users_with_phone = 0
        users = []

        # DOWNLOAD OPTION 1
        
        result = client.get_participants(request.data['channel_name'], aggressive = True)

        # DOWNLOAD OPTION 2
        # offset = 0
        # limit = 100
        # result = []

        # while True:
        #     participants = client(GetParticipantsRequest(request.data['channel_name'], ChannelParticipantsSearch(''), offset, limit,
        #         hash=0
        #     ))
        #     if not participants.users:
        #         break
        #     result.extend(participants.users)
        #     offset += len(participants.users)
                
        #     print("Download " + str(offset) + " user")

        print("Downloads done!")
        
        for usr in result:
            users.append(
                json.loads(usr.to_json())
            )

            if usr.phone is not None:
                users_with_phone += 1

        percentage = 100 * float(users_with_phone)/float(len(users))

        print("Processing done!")

        UsersInfo.objects.create(json = users)

        print("Entry done!")

        return Response({"GetPercent DONE! Count - " + str(len(users)) + " Users with phone: " + str(users_with_phone) + "(" + str(round(percentage, 2)) + "%)"}) 
 

import csv
import time
from telethon import errors

@api_view(['POST'])
def AddContact(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    phone = []    
    count = 0
    with open('file') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if(row['Phone 1 - Value']):
                txt = "".join(c for c in row['Phone 1 - Value'] if c.isalnum())
                if (txt.isdigit() and len(txt) == 11 and txt[1] == '9'):
                    phone.append(txt)
        with TelegramClient(username, api_id, api_hash) as client:
            start = time.time()
            for i in range(len(phone)):
                try:
                    time.sleep(1)
                    result = client(functions.contacts.ImportContactsRequest(
                        contacts=[InputPhoneContact(
                            client_id = 0,
                            phone = phone[i],
                            first_name = str(i),
                            last_name = str(i)
                        )]
                    ))
                    if (result.users):
                        print(phone[i] + " - доступен")
                        count += 1
                        client(functions.contacts.DeleteContactsRequest(id=[result.users[0]]))
                    else:   
                        print(phone[i] + " - НЕ ДОСТУПЕН")

                    print("Всего: " + str(i + 1) +  ", Успешно: " + str(count))
                except errors.FloodWaitError as e:
                    print('Flood wait for ', e.seconds)        
                    time.sleep(e.seconds)
            end = time.time()
    return Response({"Проверено номеров: " + str(i + 1) + ", Добавлено успешно: " + str(count) + " Затрачено времени: " + str(end - start)}) 


class ChannelInfoView(APIView):
    def get(self, request):
        return Response({"ChannelInfoView get"})






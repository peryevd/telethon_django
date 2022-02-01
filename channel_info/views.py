from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from .serializers import ChannelInfoSerializer, ArticleSerializer

from .models import ChannelInfo, UsersInfo, MessageChannel, MessageReply

from rest_framework.response import Response
from rest_framework.views import APIView
import json

from telethon.sync import TelegramClient
from telethon import functions
import asyncio

from channel_info.src.users_from_channel import *
from channel_info.src.all_users_from_reply import *
from channel_info.src.all_messages import *

 
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

class ChannelInfoView(APIView):
    api_id = api_id
    api_hash = "api_hash"

    def post(self, request):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        with TelegramClient('session_user', self.api_id, self.api_hash) as client:

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


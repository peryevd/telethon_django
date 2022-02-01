from django.urls import path, include
# from django.conf.urls import include, path
from rest_framework import routers

from .views import ChannelInfoListView, ChannelDetailView, ChannelInfoViewset, ChannelInfoView
 
api_router = routers.SimpleRouter()
api_router.register(r'channel_info', ChannelInfoViewset, basename='channel_info')

urlpatterns = [
    path('channel_info/<int:pk>/', ChannelDetailView.as_view(), name='channelinfo_detail'),
    path('', ChannelInfoListView.as_view(), name='home'),
    path(r'', include(api_router.urls)),
    path('api/', ChannelInfoView.as_view()),
]

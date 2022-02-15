from django.urls import path
from . import views

from .views import ChannelInfoListView, ChannelDetailView

urlpatterns = [
    path('channel_info/<int:pk>/', ChannelDetailView.as_view(), name='channelinfo_detail'),
    path('', ChannelInfoListView.as_view(), name='home'),
    path('api/SubNewMes', views.SubNewMes, name="SubNewMes"),
    path('api/GetChannelInfo', views.GetChannelInfo, name="GetChannelInfo"),
    path('api/GetPercent', views.GetPercent, name="GetPercent"),
    path('api/AddContact', views.AddContact, name="AddContact"),
    path('api/GetUserByFilter', views.GetUserByFilter, name="GetUserByFilter"),
]

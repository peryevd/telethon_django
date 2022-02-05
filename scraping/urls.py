from django.urls import path
from rest_framework import routers
from . import views

api_router = routers.SimpleRouter()

urlpatterns = [
    path(r'', views.index, name='index'),
    # path('api/', ChannelInfoView.as_view()),
    path('api/scrap', views.scrap, name="scrap"),
]
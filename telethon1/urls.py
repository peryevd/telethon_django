from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('channel_info.urls')), 
    path('api/', include('channel_info.urls')),
]

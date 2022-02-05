from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('scraping.urls')),
    path('api/', include('scraping.urls')),
    path('', include('channel_info.urls')), 
    path('api/', include('channel_info.urls')),
    path('admin/', admin.site.urls),
]

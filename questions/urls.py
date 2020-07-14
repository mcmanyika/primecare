from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    url(r'success/', success, name='success'),
    url(r'pending/', pending, name='pending'),
    url(r'^', covid, name='covid'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

    url(r'covid/', covid, name='covid'),
    url(r'success/', success, name='success'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

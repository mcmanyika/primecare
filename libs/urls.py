from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from libs.views import *

urlpatterns = [
    url(r'^acct-delete/(?P<id>.*)$', acct_delete, name='acct-delete'),
    url(r'^resources/', resources, name='resources'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

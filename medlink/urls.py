
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from libs.views import *
from questions.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    url(r'libs/', include('libs.urls')),
    url(r'dashboard/', include('dashboard.urls')),
    url(r'client/', include('client.urls')),

    url(r'^', include('questions.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

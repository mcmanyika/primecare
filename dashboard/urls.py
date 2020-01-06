from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import *
from libs.views import *

urlpatterns = [
    
	url(r'^main-dash/', main_dash, name='main-dash'),
    url(r'^login/', login, name='login'),
    url(r'^graphs/', graphs, name='graphs'),
    url(r'^graphs-2/', graphs_b, name='graphs-2'),
    url(r'^highchart/', highchart, name='highchart'),
    
]
from django.db import connection
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from client.models import *
from client.forms import *
from libs.models import *
from libs.forms import *

# Create your views here.

def site_index(request):
    

    context = {
        
    }    

    template = "frontend/index.html"    

    return render(request, template, context)

from django.db import connection
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required

# Create your views here.



def highchart(request):

    context = {

    }

    template = "dashboard/highchart.html"

    return render(request, template, context)

def graphs(request):

    context = {

    }

    template = "dashboard/graphs.html"

    return render(request, template, context)

def graphs_b(request):

    context = {

    }

    template = "dashboard/graphs2.html"

    return render(request, template, context)

from django.db import connection
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from libs.models import *

# Create your views here.


@login_required(login_url='/accounts/login/')
def covid(request):
    user = get_object_or_404(t_accts, rootid=request.user.id)
    if not user.status == 'Active':
        return HttpResponseRedirect('/pending/')

    form = CovidForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect('/success/')

    context = {
        "user": user,
        'form': form,
    }
    template = "questions/covid.html"

    return render(request, template, context)


def success(request):
    user = get_object_or_404(t_accts, rootid=request.user.id)
    context = {
        "user": user,
    }
    template = "questions/success.html"

    return render(request, template, context)


def pending(request):
    user = get_object_or_404(t_accts, rootid=request.user.id)

    context = {
        "user": user,
    }
    template = "questions/pending.html"

    return render(request, template, context)

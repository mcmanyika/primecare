#import requests
import uuid
import json
import math
import datetime
from django.db import connection
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Count
from joins.forms import User
from django.contrib.auth.decorators import login_required
from joins.forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from joins.models import *
from libs.models import *


# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def register_view(request):
    now = datetime.datetime.now()

    form = UserRegisterForm(request.POST or None)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                user_p = get_object_or_404(t_acct, rootid=request.user.id)
                if user_p.status == 'Active':
                    return HttpResponseRedirect('/questions/covid/')
                else:
                    return HttpResponseRedirect('/questions/pending/')
            else:
                messages.success(request, "Enter correct username or password")

    if request.method == 'POST':
        passchange = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            passchange_user = user.save()
            update_session_auth_hash(request, user)
            messages.success(request, _(
                'Your password was successfully updated!'))
            return redirect('change_password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        passchange = PasswordChangeForm(request.user)

    context = {
        "form": form,
        "passchange": passchange,
    }
    return render(request, "dashboard/login.html", context)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/joins/user-profile/')
    else:
        form = SignUpForm()

    context = {
        "form": form,
    }
    return render(request, 'joins/register.html', context)


def Userprofile(request):

    form = ProfileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect('/joins/pending/')

    context = {
        "form": form,
    }

    template = "joins/profile.html"
    return render(request, template, context)


def pending(request):
    user = get_object_or_404(t_acct, rootid=request.user.id)

    context = {
        "user": user,
    }
    template = "joins/pending.html"

    return render(request, template, context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user-img')
    else:
        form = SignUpForm()
    return render(request, 'joins/signup.html', {'form': form})


def signup_confirmation(request):

    return render(request, 'signup_confirmation.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _(
                'Your password was successfully updated!'))
            return redirect('change_password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def staff(request):
    dictionary = t_dict.objects.all()
    url = t_url.objects.raw("""SELECT u.id, u.icon, u.url, u.header, u.category
                                FROM libs_t_url u
                            """)

    sub_url = t_sub_url.objects.raw("""SELECT su.id, su.rootid_id, su.title
                                       FROM libs_t_sub_url su
                                    """)

    accts = t_acct.objects.raw("""SELECT a.id, a.first_name, a.last_name, ea.rootid,  ea.gender, ea.phone, 
									 ea.address,
									 ea.emergency_contact,  ea.account_type, ea.status
									FROM auth_user a
									INNER JOIN joins_t_acct ea ON ea.rootid = a.id
                                    WHERE ea.account_type = 'Attendant' And ea.status= 'Active'
                                """)

    context = {
        "dictionary": dictionary,
        "url": url,
        "sub_url": sub_url,
        "accts": accts,

    }

    template = "joins/staff.html"

    return render(request, template, context)


@login_required(login_url='/login/')
def staff_detail(request, id):
    dictionary = t_dict.objects.all()
    url = t_url.objects.raw("""SELECT u.id, u.icon, u.url, u.header, u.category
                                FROM libs_t_url u
                            """)

    sub_url = t_sub_url.objects.raw("""SELECT su.id, su.rootid_id, su.title
                                       FROM libs_t_sub_url su
                                    """)
    instance = get_object_or_404(t_acct, rootid=id)
    client = User.objects.raw("""SELECT u.id, u.first_name, u.last_name, a.rootid,
                                a.gender, a.phone, 
                                a.address,
                                a.emergency_contact, a.account_type, a.status
                                FROM auth_user u
                                INNER JOIN joins_t_acct a ON a.rootid = u.id
                                WHERE  a.id = %s """, [instance.id])

    EditAcctform = EditAcctForm(
        request.POST or None, request.FILES or None, instance=instance)
    if EditAcctform.is_valid():
        f = EditAcctform.save(commit=False)
        f.save()

    context = {
        "dictionary": dictionary,
        "url": url,
        "sub_url": sub_url,
        "EditAcctform": EditAcctform,

        "id": instance.id,
        "gender": instance.gender,
        "phone": instance.phone,
        "address": instance.address,
        "emergency_contact": instance.emergency_contact,
        "account_type": instance.account_type,
        "status": instance.status,


        "client": client,

    }

    template = "joins/staff_detail.html"

    return render(request, template, context)


@login_required(login_url='/login/')
def client(request):
    dictionary = t_dict.objects.all()
    url = t_url.objects.raw("""SELECT u.id, u.icon, u.url, u.header, u.category
                                FROM libs_t_url u
                            """)

    sub_url = t_sub_url.objects.raw("""SELECT su.id, su.rootid_id, su.title
                                       FROM libs_t_sub_url su
                                    """)

    accts = t_acct.objects.raw("""SELECT a.id, a.first_name, a.last_name, ea.rootid,  ea.gender, ea.phone, 
									 ea.address,
									 ea.emergency_contact,  ea.account_type, ea.status
									FROM auth_user a
									INNER JOIN joins_t_acct ea ON ea.rootid = a.id
                                    WHERE ea.account_type = 'Client' And ea.status= 'Active'
                                """)

    context = {
        "dictionary": dictionary,
        "url": url,
        "sub_url": sub_url,
        "accts": accts,

    }

    template = "joins/client.html"

    return render(request, template, context)


@login_required(login_url='/login/')
def client_detail(request, id):
    dictionary = t_dict.objects.all()
    url = t_url.objects.raw("""SELECT u.id, u.icon, u.url, u.header, u.category
                                FROM libs_t_url u
                            """)

    sub_url = t_sub_url.objects.raw("""SELECT su.id, su.rootid_id, su.title
                                       FROM libs_t_sub_url su
                                    """)
    instance = get_object_or_404(t_acct, rootid=id)
    client = User.objects.raw("""SELECT u.id, u.first_name, u.last_name, a.rootid,
                                a.dob, a.gender, a.phone, 
                                a.address,
                                a.emergency_contact, a.account_type, a.status
                                FROM auth_user u
                                INNER JOIN joins_t_acct a ON a.rootid = u.id
                                WHERE  a.id = %s """, [instance.id])

    EditAcctform = EditAcctForm(
        request.POST or None, request.FILES or None, instance=instance)
    if EditAcctform.is_valid():
        f = EditAcctform.save(commit=False)
        f.save()

    context = {
        "dictionary": dictionary,
        "url": url,
        "sub_url": sub_url,
        "EditAcctform": EditAcctform,

        "id": instance.id,
        "gender": instance.gender,
        "phone": instance.phone,
        "address": instance.address,
        "emergency_contact": instance.emergency_contact,
        "account_type": instance.account_type,
        "status": instance.status,


        "client": client,

    }

    template = "joins/client_detail.html"

    return render(request, template, context)

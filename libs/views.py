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
from libs.models import *
from libs.forms import *
from joins.forms import *
from questions.models import *
from questions.forms import *


# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


@login_required(login_url='/login/')
def resources(request):

    dictionary = t_dict.objects.all()
    resources = t_resources.objects.all()

    url = t_url.objects.raw("""SELECT u.id, u.icon, u.url, u.header, u.category
                                FROM libs_t_url u
                            """)

    sub_url = t_sub_url.objects.raw("""SELECT su.id, su.rootid_id, su.title
                                       FROM libs_t_sub_url su
                                    """)

    form = ResourceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        # return HttpResponseRedirect('/confirmation/')
    context = {
        "resources": resources,
        "dictionary": dictionary,
        "url": url,
        "sub_url": sub_url,
        "form": form,

    }

    template = "libs/resources.html"

    return render(request, template, context)


def acct_delete(request, id):
    obj = get_object_or_404(t_acct, id)
    obj.delete()

    context = {
        "object": obj,
    }

    template = "acct_delete.html"

    return render(request, template, context)


def covid(request):
    dictionary = t_dict.objects.all()

    url = t_url.objects.raw("""SELECT u.id, u.icon, u.url, u.header, u.category
                                FROM libs_t_url u
                            """)
    sub_url = t_sub_url.objects.raw("""SELECT su.id, su.rootid_id, su.title
                                       FROM libs_t_sub_url su
                                    """)

    form = CovidForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect('/dashboard/main-dash/')

    context = {
        "url": url,
        "sub_url": sub_url,
        'form': form,
    }
    template = "libs/covid.html"

    return render(request, template, context)


class AcctDelete(DeleteView):
    template = "acct_delete.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(t_acct, id=id_)

    def get_success_url(self):
        return reverse('client')

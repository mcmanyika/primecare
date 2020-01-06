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

def employee_dash(request):
    client = t_care_giver.objects.raw("""SELECT c.id, c.fname, c.lname, tc.Daily_Login_ID, tc.user, tc.timestamp
                                         FROM client_t_client c
                                         INNER JOIN libs_client tc ON tc.PatientID = c.id
                                         WHERE tc.user = %s ORDER BY tc.timestamp DESC LIMIT 1; """, [request.user.id])
    
    


    form = EmployeeSignOutForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect('/')

    context = {
       "form" : form,
       "client" : client,
        
    }    

    template = "client/employee_dash.html"    

    return render(request, template, context)




def billing_tracker(request):
    accts = t_accts.objects.raw("""
                                    SELECT a.id, ca.rootid_id, a.fname, a.lname, ca.client_number, a.account_type
                                    FROM joins_t_accts a
                                    INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                """)

    BillingTracker = t_billing_tracker.objects.raw("""SELECT ca.rootid_id, bt.claim_id, bt.id,  a.fname, a.lname, ca.client_number, a.account_type,
                                                     bt.service_date_from,bt.service_date_to, bt.amount_billed, bt.amount_paid,
                                                     bt.payment_status
                                                FROM joins_t_accts a
                                                INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                                INNER JOIN client_t_billing_tracker bt ON bt.client_number = ca.client_number 
                                                ORDER BY bt.id Desc""")

    context = {
    "accts": accts,
    "BillingTracker" : BillingTracker,
        
    }    

    template = "client/billing_tracker.html"    

    return render(request, template, context)

def billing_tracker_detail(request, id):

    instance = get_object_or_404(t_billing_tracker, id=id)

    form = BillingTrackerForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect('/confirmation/')

    context = {
        "form" : form,
        
    }    

    template = "client/billing_tracker_detail.html"    

    return render(request, template, context)


def edit_billing_tracker(request, id):
    dictionary = t_dict.objects.all()
    instance = get_object_or_404(t_billing_tracker, id=id)

    form = EditBillingTrackerForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        # return HttpResponseRedirect('/confirmation/')

    context = {
        "dictionary" : dictionary,
        "form" : form,
        "claim_id" : instance.claim_id,
        "service_date_from" : instance.service_date_from,
        "service_date_to" : instance.service_date_to,
        "rootid" : instance.rootid_id,
        "client_number" : instance.client_number,
        "payment_status" : instance.payment_status,
        
    }     

    template = "client/edit_billing_tracker.html"    

    return render(request, template, context)



def billing_delete(request, id):
    obj = get_object_or_404(t_billing_tracker, id=id)
    obj.delete()

    context = {
        "object" : obj,
    }

    template = "client/billing_delete.html"

    return render(request, template, context)



def add_client (request):
    client = t_client.objects.all().order_by('-id')
    dictionary = t_dict.objects.all()

    form = AddClientForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        # return HttpResponseRedirect('/staff-dashboard/')


    context = {
        "dictionary" : dictionary,
       "client" : client,
       "forms" : forms,
        
    }    

    template = "add_clients.html"    

    return render(request, template, context)

def daily_logs(request):
    client = t_client.objects.all().order_by('-id')
    logs = t_care_giver.objects.raw("""SELECT c.id, c.fname, c.lname, 
                                            tc.id, tc.Daily_Login_ID, 
                                            tc.Daily_Logout_ID,
                                         tc.user, tc.timestamp
                                         FROM client_t_client c
                                         INNER JOIN libs_client tc ON tc.PatientID = c.id
                                         GROUP BY c.id, tc.timestamp
                                         ORDER BY tc.id DESC """)

    context = {
       "logs" : logs,
       "client" : client,
        
    }    

    template = "daily_logs.html"    

    return render(request, template, context)


def claims(request):
    claims = t_accts.objects.raw("""
                                    SELECT a.id, a.fname, a.lname, b.batch_id, b.id as billing_id, b.billing_date, ba.id, ba.payment_date, ba.status
                                    FROM joins_t_accts a
                                    INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                    INNER JOIN client_t_bill b ON b.client_number = ca.client_number
                                    LEFT JOIN client_t_batch ba ON ba.rootid_id = b.id 
                                    ORDER BY b.id DESC
                                """)

    accts = t_accts.objects.raw("""SELECT a.id, ca.rootid_id, a.fname, a.middle_name, a.lname,a.gender, 
                                    a.dob, a.phone, a.address, a.emergency_contact, 
                                    ca.client_number, ca.soc, a.account_type
                                    FROM joins_t_accts a
                                    INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                """)
   

    context = {
    "claims": claims,
    "accts" : accts,
        
    }    

    template = "client/claims.html"    

    return render(request, template, context)

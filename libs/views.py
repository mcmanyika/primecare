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
from client.models import *
from client.forms import *
from survey.models import *
from survey.forms import *


# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def employee_signin(request):

    staff = t_accts.objects.raw("""SELECT a.id, a.fname, a.lname
	                                     FROM joins_t_accts a
	                                     WHERE a.user = %s """, [request.user.id])

    form = EmployeeSignInForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect('/client/employee-dash/')

    context = {
        "staff": staff,
        "form": form,
    }

    template = "add_daily_rec.html"

    return render(request, template, context)


def employee_signout(request):

    form = EmployeeSignOutForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect('/')

    context = {
        "form": form,
    }

    template = "employee_signout.html"

    return render(request, template, context)


@login_required(login_url='/login/')
def staff_dashboard(request):
    accts = t_accts.objects.raw("""
                                    SELECT a.id, ea.rootid_id, a.fname, a.lname, ea.employee_id, a.account_type
                                    FROM joins_t_accts a
                                    INNER JOIN joins_t_employee_attribute ea ON ea.rootid_id = a.id
                                """)
    context = {
        "staff": staff,

    }

    template = "staff.html"

    return render(request, template, context)


@login_required(login_url='/login/')
def staff(request):
    dictionary = t_dict.objects.all()
    url = t_url.objects.raw("""SELECT u.id, u.icon, u.url, u.header, u.category
                                FROM libs_t_url u
                            """)

    sub_url = t_sub_url.objects.raw("""SELECT su.id, su.rootid_id, su.title
                                       FROM libs_t_sub_url su
                                    """)

    VisitTracker = t_visit_tracker.objects.all().order_by('-id')
    accts = t_accts.objects.raw("""SELECT a.id, ea.rootid_id, a.fname, a.lname, a.dob, a.gender, a.phone, 
									 a.address,ea.doh,
									 a.emergency_contact, ea.employee_id, a.account_type
									FROM joins_t_accts a
									INNER JOIN joins_t_employee_attribute ea ON ea.rootid_id = a.id
                                """)

    paginator = Paginator(accts, 100)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    billinghistory = t_bill.objects.raw("""SELECT b.id, b.client_number, b.billing_date
                                            FROM client_t_bill b
                                            ORDER BY b.id Desc""")

    c = connection.cursor()
    c.cursor.execute("""SELECT a.id , count(a.id) as count, a.gender
                                     FROM joins_t_accts a
                                    INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                     GROUP BY a.gender""")
    c = dictfetchall(c)
    totalFemale = c[0]['count'] if c else 0
    totalMen = c[1]['count'] if c else 0
    totalCount = (totalFemale + totalMen)

    ta = connection.cursor()
    ta.cursor.execute("""SELECT b.id, sum(b.amount_billed) as total_billed, sum(b.amount_paid) as total_paid
                         FROM client_t_billing_tracker b
                      """)
    ta = dictfetchall(ta)
    total_billed = ta[0]['total_billed'] if ta else 0
    total_paid = ta[0]['total_paid'] if ta else 0

    if total_billed and total_paid:
        balance = (total_billed - total_paid)
    else:
        balance = 0
        total_paid = 0
        total_billed = 0

    context = {
        "dictionary": dictionary,
        "accts": queryset,
        "VisitTracker": VisitTracker,
        "url": url,
        "sub_url": sub_url,
        "balance": balance,
        "total_paid": total_paid,
        "total_billed": total_billed,
        "totalMen": totalMen,
        "totalFemale": totalFemale,

    }

    template = "staff.html"

    return render(request, template, context)


@login_required(login_url='/login/')
def staff_detail(request, id):
    instance = get_object_or_404(t_accts, id=id)
    client = t_care_giver.objects.raw("""SELECT cg.id, cg.client_id, cg.care_attendant, c.fname, c.lname 
										FROM client_t_care_giver cg
										INNER JOIN client_t_client c ON c.id = cg.client_id
                                        WHERE cg.care_attendant = %s """, [instance.id])

    oig = t_oig.objects.raw("""SELECT og.id, og.rootid_id, og.document, og.timestamp 
                                        FROM libs_t_oig og 
                                        WHERE og.rootid_id = %s ORDER BY og.id DESC""", [instance.id])

    EditAcctform = EditAcctForm(
        request.POST or None, request.FILES or None, instance=instance)
    if EditAcctform.is_valid():
        f = EditAcctform.save(commit=False)
        f.save()

    form = CareGiverForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")

    exclusionform = ExclusionForm(request.POST or None, request.FILES or None)
    if exclusionform.is_valid():
        f = exclusionform.save(commit=False)
        f.save()
        messages.success(request, "Saved")

    context = {
        "EditAcctform": EditAcctform,
        "form": form,
        "exclusionform": exclusionform,
        "oig": oig,
        "id": instance.id,
        "fname": instance.fname,
        "middle_name": instance.middle_name,
        "lname": instance.lname,
        "gender": instance.gender,
        "phone": instance.phone,
        "address": instance.address,
        "email": instance.email,
        "emergency_contact": instance.emergency_contact,

        "client": client,

    }

    template = "staff_detail.html"

    return render(request, template, context)


def add_staff(request):
    dictionary = t_dict.objects.all().order_by('-id')

    form = AcctForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect('/staff-dashboard/')

    context = {
        "form": form,
        "dictionary": dictionary,


    }

    template = "add_staff.html"

    return render(request, template, context)


@login_required(login_url='/')
def main_dash(request):
    dictionary = t_dict.objects.all()

    url = t_url.objects.raw("""SELECT u.id, u.icon, u.url, u.header, u.category
                                FROM libs_t_url u
                            """)
    sub_url = t_sub_url.objects.raw("""SELECT su.id, su.rootid_id, su.title
                                       FROM libs_t_sub_url su
                                    """)

    covid = t_questionnaire.objects.raw("""SELECT q.id, a.fname, a.lname, q.timestamp
                                       FROM survey_t_questionnaire q
                                       INNER JOIN joins_t_accts a ON a.id = q.user
                                       Limit 6
                                    """)

    accts = t_accts.objects.raw("""SELECT a.id, ca.rootid_id, a.fname, a.middle_name, a.lname,a.gender, 
                                    a.dob, a.phone, a.address, a.emergency_contact, 
                                    ca.client_number, ca.soc, a.account_type
                                    FROM joins_t_accts a
                                    INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                """)

    paginator = Paginator(accts, 6)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    BillingTracker = t_billing_tracker.objects.raw("""SELECT ca.rootid_id, bt.id,  a.fname, a.lname, ca.client_number, a.account_type,
                                                     bt.service_date_from, bt.service_date_to,
                                                     bt.notes,
                                                     bt.payment_status
                                                FROM joins_t_accts a
                                                INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                                INNER JOIN client_t_billing_tracker bt ON bt.client_number = ca.client_number 

                                                ORDER BY bt.id Desc
                                                Limit 6""")

    billinghistory = t_bill.objects.raw("""SELECT b.id, b.client_number, b.billing_date
                                            FROM client_t_bill b
                                            ORDER BY b.id Desc""")

    c = connection.cursor()
    c.cursor.execute("""SELECT a.id , count(a.id) as count, a.gender
                                     FROM joins_t_accts a
                                    INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                     GROUP BY a.gender""")
    c = dictfetchall(c)
    totalFemale = c[0]['count'] if c else 0
    totalMen = c[1]['count'] if c else 0
    totalCount = (totalFemale + totalMen)

    ta = connection.cursor()
    ta.cursor.execute("""SELECT b.id, sum(b.amount_billed) as total_billed, sum(b.amount_paid) as total_paid
                         FROM client_t_billing_tracker b
                      """)
    ta = dictfetchall(ta)
    total_billed = ta[0]['total_billed'] if ta else 0
    total_paid = ta[0]['total_paid'] if ta else 0

    if total_billed:
        balance = (total_billed - total_paid)
    else:
        balance = 0
        total_paid = 0
        total_billed = 0

    payment_track = t_bill.objects.raw("""SELECT bt.id, b.billing_date, ca.company, bt.payment_status, 
                                                  bt.amount_billed, bt.amount_paid
                                            FROM client_t_billing_tracker bt
                                            INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = bt.rootid_id
                                            INNER JOIN client_t_bill b ON b.rootid = bt.rootid_id
                                            GROUP BY b.billing_date, bt.payment_status, ca.company""")

    form = BillingTrackerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")

    billform = BillForm(request.POST or None, request.FILES or None)
    if billform.is_valid():
        f = billform.save(commit=False)
        f.save()
        messages.success(request, "Saved")

    context = {
        "url": url,
        "sub_url": sub_url,
        "dictionary": dictionary,
        "form": form,
        "covid": covid,
        "billform": billform,
        "payment_track": payment_track,
        "BillingTracker": BillingTracker,
        "billinghistory": billinghistory,
        "accts": queryset,
        "gender": c,
        "totalMen": totalMen,
        "totalFemale": totalFemale,
        "total_billed": total_billed,
        "total_paid": total_paid,
        "balance": balance,

    }

    template = "client/dashboard.html"

    return render(request, template, context)


@login_required(login_url='/')
def client(request):
    dictionary = t_dict.objects.all()

    last_billed = t_bill.objects.all().order_by('-timestamp')

    url = t_url.objects.raw("""SELECT u.id, u.icon, u.url, u.header, u.category
                                FROM libs_t_url u
                            """)

    sub_url = t_sub_url.objects.raw("""SELECT su.id, su.rootid_id, su.title
                                       FROM libs_t_sub_url su
                                    """)

    accts = t_accts.objects.raw("""SELECT a.id, ca.rootid_id, a.fname, a.middle_name, a.lname,a.gender, 
                                    a.dob, a.phone, a.address, a.emergency_contact, 
                                    ca.client_number, ca.company, ca.soc, a.account_type
                                    FROM joins_t_accts a
                                    INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                    ORDER BY a.fname 

                                """)

    # paginator = Paginator(accts, 40)  # Show 25 contacts per page

    # page_request_var = "page"
    # page = request.GET.get('page')
    # try:
    #     queryset = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     queryset = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     queryset = paginator.page(paginator.num_pages)

    query = request.GET.get("q")
    if query:
        queryset = accts.filter(
            Q(fname__icontains=query) |
            Q(lname__icontains=query)
        ).distinct()

    BillingTracker = t_billing_tracker.objects.raw("""SELECT ca.rootid_id, bt.id,  a.fname, a.lname, ca.client_number, a.account_type,
                                                     bt.service_date_from, bt.service_date_to,
                                                     bt.notes,
                                                     bt.payment_status
                                                FROM joins_t_accts a
                                                INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                                INNER JOIN client_t_billing_tracker bt ON bt.client_number = ca.client_number 
                                                ORDER BY bt.id Desc""")

    billinghistory = t_bill.objects.raw("""SELECT b.id, b.billing_date
                                            FROM client_t_bill b
                                            ORDER BY b.id Desc
                                            """)

    c = connection.cursor()
    c.cursor.execute("""SELECT a.id , count(a.id) as count, a.gender
                                     FROM joins_t_accts a
                                    INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                     GROUP BY a.gender""")
    c = dictfetchall(c)
    totalFemale = c[0]['count'] if c else 0
    totalMen = c[1]['count'] if c else 0
    totalCount = (totalFemale + totalMen)

    ta = connection.cursor()
    ta.cursor.execute("""SELECT b.id, sum(b.amount_billed) as total_billed, sum(b.amount_paid) as total_paid
                         FROM client_t_billing_tracker b
                      """)
    ta = dictfetchall(ta)
    total_billed = ta[0]['total_billed'] if ta else 0
    total_paid = ta[0]['total_paid'] if ta else 0

    if total_billed and total_paid:
        balance = (total_billed - total_paid)
    else:
        balance = 0
        total_paid = 0
        total_billed = 0

    form = BillingTrackerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")

    billform = BillForm(request.POST or None, request.FILES or None)
    if billform.is_valid():
        f = billform.save(commit=False)
        f.save()
        messages.success(request, "Saved")

    context = {
        "url": url,
        "sub_url": sub_url,
        "dictionary": dictionary,
        "form": form,
        "billform": billform,
        "BillingTracker": BillingTracker,
        "billinghistory": billinghistory,
        "accts": accts,
        "last_billed": last_billed,
        "gender": c,
        "totalMen": totalMen,
        "totalFemale": totalFemale,
        "total_billed": total_billed,
        "total_paid": total_paid,
        "balance": balance,

    }

    template = "client/client.html"

    return render(request, template, context)


@login_required(login_url='/')
def client_detail(request, id):
    instance = get_object_or_404(t_accts, pk=id)
    inst = get_object_or_404(t_client_attribute, rootid_id=instance.id)
    billinghistory = t_billing_tracker.objects.raw("""SELECT b.id, ca.rootid_id, a.fname, a.lname, b.payment_status, b.claim_id, 
                                            b.service_date_from, b.service_date_to,
                                            b.amount_billed, b.amount_paid
                                            FROM joins_t_accts a
                                            INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                            INNER JOIN client_t_billing_tracker b ON b.rootid_id = ca.rootid_id
                                            WHERE ca.rootid_id = %s ORDER BY b.id DESC""", [instance.id])

    form = CareGiverForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")

    EditAcctform = EditAcctForm(
        request.POST or None, request.FILES or None, instance=instance)
    if EditAcctform.is_valid():
        f = EditAcctform.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        # return HttpResponseRedirect('/signup-confirmation/')

    ClientAttributeForm = EditClientAttributeForm(
        request.POST or None, request.FILES or None, instance=inst)
    if ClientAttributeForm.is_valid():
        form = ClientAttributeForm.save(commit=False)
        form.save()
        messages.success(request, "Saved")
    context = {
        "form": form,
        "EditAcctform": EditAcctform,
        "ClientAttributeForm": ClientAttributeForm,
        "id": instance.id,
        "fname": instance.fname,
        "middle_name": instance.middle_name,
        "lname": instance.lname,
        "gender": instance.gender,
        "dob": instance.dob,
        "phone": instance.phone,
        "address": instance.address,
        "emergency_contact": instance.emergency_contact,
        "billinghistory": billinghistory,

    }

    template = "client/client_detail.html"

    return render(request, template, context)


def client_attribute_detail(request, id):
    instance = get_object_or_404(t_client_attribute, rootid_id=id)
    dictionary = t_dict.objects.all()

    ClientAttributeForm = EditClientAttributeForm(
        request.POST or None, request.FILES or None, instance=instance)
    if ClientAttributeForm.is_valid():
        form = ClientAttributeForm.save(commit=False)
        form.save()
        messages.success(request, "Saved")
    context = {
        "dictionary": dictionary,
        "ClientAttributeForm": ClientAttributeForm,
        "company": instance.company,

    }

    template = "client/client_attribute_detail.html"

    return render(request, template, context)


@login_required(login_url='/')
def billing(request):
    dictionary = t_dict.objects.all()

    url = t_url.objects.raw("""SELECT u.id, u.icon, u.url, u.header, u.category
                                FROM libs_t_url u
                            """)
    sub_url = t_sub_url.objects.raw("""SELECT su.id, su.rootid_id, su.title
                                       FROM libs_t_sub_url su
                                    """)

    billing = t_billing_tracker.objects.raw("""SELECT ca.rootid_id, bt.id,  a.fname, a.lname, ca.client_number, a.account_type,
                                                     bt.service_date_from, bt.service_date_to,
                                                     bt.notes,
                                                     bt.payment_status, bt.amount_billed, bt.amount_paid
                                                FROM joins_t_accts a
                                                INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                                INNER JOIN client_t_billing_tracker bt ON bt.client_number = ca.client_number 
                                                ORDER BY bt.id Desc""")

    billinghistory = t_bill.objects.raw("""SELECT b.id, b.client_number, b.billing_date
                                            FROM client_t_bill b
                                            ORDER BY b.id Desc""")

    c = connection.cursor()
    c.cursor.execute("""SELECT a.id , count(a.id) as count, a.gender
                                     FROM joins_t_accts a
                                    INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                     GROUP BY a.gender""")
    c = dictfetchall(c)
    totalFemale = c[0]['count'] if c else 0
    totalMen = c[1]['count'] if c else 0
    totalCount = (totalFemale + totalMen)

    ta = connection.cursor()
    ta.cursor.execute("""SELECT b.id, sum(b.amount_billed) as total_billed, sum(b.amount_paid) as total_paid
                         FROM client_t_billing_tracker b
                      """)
    ta = dictfetchall(ta)
    total_billed = ta[0]['total_billed'] if ta else 0
    total_paid = ta[0]['total_paid'] if ta else 0

    if total_billed and total_paid:
        balance = (total_billed - total_paid)
    else:
        balance = 0
        total_paid = 0
        total_billed = 0

    form = BillingTrackerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")

    billform = BillForm(request.POST or None, request.FILES or None)
    if billform.is_valid():
        f = billform.save(commit=False)
        f.save()
        messages.success(request, "Saved")

    context = {
        "url": url,
        "sub_url": sub_url,
        "dictionary": dictionary,
        "form": form,
        "billform": billform,
        "billinghistory": billinghistory,
        "billing": billing,
        "gender": c,
        "totalMen": totalMen,
        "totalFemale": totalFemale,
        "total_billed": total_billed,
        "total_paid": total_paid,
        "balance": balance,

    }

    template = "client/billing.html"

    return render(request, template, context)


def batch_detail(request, id):
    dictionary = t_dict.objects.all().order_by('-id')
    instance = get_object_or_404(t_bill, id=id)
    batch = t_billing_tracker.objects.raw("""SELECT ba.id, ba.rootid_id, ba.status, ba.billing_date, ba.payment_date, ba.notes,  ba.timestamp
											FROM client_t_bill b
											INNER JOIN client_t_batch ba ON ba.rootid_id = b.id 
											WHERE b.rootid_id = %s ORDER BY ba.id DESC""", [instance.id])

    form = BatchForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")

    context = {
        "dictionary": dictionary,
        "form": form,
        "rootid": instance.id,
        "bill_date": instance.billing_date,
        "batch_id": instance.batch_id,
        "batch": batch,

    }

    template = "client/batch_detail.html"

    return render(request, template, context)


def edit_batch_detail(request, id):
    dictionary = t_dict.objects.all().order_by('-id')
    instance = get_object_or_404(t_bill, id=id)

    form = BatchForm(request.POST or None,
                     request.FILES or None, instance=instance)
    if form.is_valid():
        f = form.save(commit=False)
        f.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect('/confirmation/')

    context = {
        "dictionary": dictionary,
        "batch_id": instance.batch_id,
        "form": form,

    }

    template = "client/edit_batch_detail.html"

    return render(request, template, context)


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

    BillingTracker = t_billing_tracker.objects.raw("""SELECT ca.rootid_id, bt.id,  a.fname, a.lname, ca.client_number, a.account_type,
                                                     bt.service_date_from, bt.service_date_to,
                                                     bt.notes,
                                                     bt.payment_status
                                                FROM joins_t_accts a
                                                INNER JOIN joins_t_client_attribute ca ON ca.rootid_id = a.id
                                                INNER JOIN client_t_billing_tracker bt ON bt.client_number = ca.client_number 
                                                ORDER BY bt.id Desc""")

    billinghistory = t_bill.objects.raw("""SELECT b.id, b.client_number, b.billing_date
                                            FROM client_t_bill b
                                            ORDER BY b.id Desc""")
    ta = connection.cursor()
    ta.cursor.execute("""SELECT b.id, sum(b.amount_billed) as total_billed, sum(b.amount_paid) as total_paid
                         FROM client_t_billing_tracker b
                      """)
    ta = dictfetchall(ta)
    total_billed = ta[0]['total_billed'] if ta else 0
    total_paid = ta[0]['total_paid'] if ta else 0

    if total_billed and total_paid:
        balance = (total_billed - total_paid)
    else:
        balance = 0
        total_paid = 0
        total_billed = 0

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
        "BillingTracker": BillingTracker,
        "billinghistory": billinghistory,
        "balance": balance,
        "form": form,

    }

    template = "libs/resources.html"

    return render(request, template, context)


def acct_delete(request, id):
    obj = get_object_or_404(t_accts, id)
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


# class AcctListView(ListView):
#     template = 'client/acct_list.html'
#     queryset = t_accts.objects.all()


class AcctDelete(DeleteView):
    template = "acct_delete.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(t_accts, id=id_)

    def get_success_url(self):
        return reverse('client')

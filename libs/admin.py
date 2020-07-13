from django.contrib import admin
from libs.models import *

# Register your models here.


class AcctsAdmin(admin.ModelAdmin):
    list_display = ['rootid', 'gender', 'dob']

    class Meta:
        model = t_accts


admin.site.register(t_accts, AcctsAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ['PatientID']

    class Meta:
        model = Client


admin.site.register(Client, ClientAdmin)


class PatientAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname']

    class Meta:
        model = t_patient_acct


admin.site.register(t_patient_acct, PatientAdmin)


class DictAdmin(admin.ModelAdmin):
    list_display = ['header', 'category', 'status']

    class Meta:
        model = t_dict


admin.site.register(t_dict, DictAdmin)


class VisitTrackerAdmin(admin.ModelAdmin):
    list_display = ['rootid', 'date', 'employee_id', 'status', 'timestamp']

    class Meta:
        model = t_visit_tracker


admin.site.register(t_visit_tracker, VisitTrackerAdmin)


class ExclusionAdmin(admin.ModelAdmin):
    list_display = ['rootid',  'timestamp']

    class Meta:
        model = t_oig


admin.site.register(t_oig, ExclusionAdmin)


class UrlAdmin(admin.ModelAdmin):
    list_display = ['header', 'category', 'status', 'timestamp']

    class Meta:
        model = t_url


admin.site.register(t_url, UrlAdmin)


class SubUrlAdmin(admin.ModelAdmin):
    list_display = ['title', 'status',  'timestamp']

    class Meta:
        model = t_sub_url


admin.site.register(t_sub_url, SubUrlAdmin)


class ResourcesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category',  'timestamp']

    class Meta:
        model = t_resources


admin.site.register(t_resources, ResourcesAdmin)

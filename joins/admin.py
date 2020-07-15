from django.contrib import admin

from .models import *


# Register your models here.

class UserPicAdmin(admin.ModelAdmin):
    list_display = ['id', ]

    class Meta:
        model = UserProfile


admin.site.register(UserProfile, UserPicAdmin)


class AcctsAdmin(admin.ModelAdmin):
    list_display = ['id',  'gender', 'account_type', 'status']

    class Meta:
        model = t_accounts


admin.site.register(t_accounts, AcctsAdmin)


class EmployeeAttributeAdmin(admin.ModelAdmin):
    list_display = ['rootid', 'employee_id', 'doh', 'status']

    class Meta:
        model = t_employee_attribute


admin.site.register(t_employee_attribute, EmployeeAttributeAdmin)


class ClientAttributeAdmin(admin.ModelAdmin):
    list_display = ['rootid', 'client_number', 'company', 'soc', 'status']

    class Meta:
        model = t_client_attribute


admin.site.register(t_client_attribute, ClientAttributeAdmin)


class EvaluationAttributeAdmin(admin.ModelAdmin):
    list_display = ['rootid', 'employee_id', 'scheduled_date', 'status']

    class Meta:
        model = t_evaluation


admin.site.register(t_evaluation, EvaluationAttributeAdmin)

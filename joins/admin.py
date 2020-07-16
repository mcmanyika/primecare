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
        model = t_acct


admin.site.register(t_acct, AcctsAdmin)

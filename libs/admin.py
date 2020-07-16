from django.contrib import admin
from libs.models import *

# Register your models here.


class DictAdmin(admin.ModelAdmin):
    list_display = ['header', 'category', 'status']

    class Meta:
        model = t_dict


admin.site.register(t_dict, DictAdmin)


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


class AcctAdmin(admin.ModelAdmin):
    list_display = ['id',  'gender', 'account_type', 'status']

    class Meta:
        model = accts


admin.site.register(accts, AcctAdmin)

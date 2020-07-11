from django.contrib import admin
from .models import *

# Register your models here.


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['id', 'q1', 'q2']

    class Meta:
        t_questionnaire


admin.site.register(t_questionnaire, QuestionnaireAdmin)
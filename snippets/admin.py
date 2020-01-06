from django.contrib import admin
from snippets.models import *

# Register your models here.

class SnippetAdmin(admin.ModelAdmin):
	list_display = [ 'title', 'timestamp']
	class Meta:
		model = Snippets
admin.site.register(Snippets, SnippetAdmin)
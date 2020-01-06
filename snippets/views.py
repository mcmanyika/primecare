from django.shortcuts import render
from django.utils import timezone
from .models import Snippets
from django.views import View
from django.views.generic import ListView, DetailView

# Create your views here.

class SnippetListView(ListView):
	model = Snippets
	template_name = 'snippets/snippet_list.html'

	def get_context_data(self, **kwargs):
		snippet_list = Snippets.objects.all()
		context = {
			"snippet_list" : snippet_list,
		}
		return context


class SnippetDetailView(DetailView):
	model = Snippets
	template_name = 'snippets/snippet_detail.html'
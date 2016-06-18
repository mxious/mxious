from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
	""" Renders the home view. """
	template_name = 'pages/home.html'
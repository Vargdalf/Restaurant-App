from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'


class PanelView(TemplateView):
    template_name = 'panel.html'

class StatView(TemplateView):
    template_name = 'stats.html'

class WaiterView(TemplateView):
    template_name = 'waiter.html'
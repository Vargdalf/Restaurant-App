from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class PanelView(TemplateView):
    template_name = 'panel.html'
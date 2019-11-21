from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView

from arepo.forms import NewOrderForm
from arepo.models import Order


class HomePageView(TemplateView):
    template_name = 'home.html'


class PanelView(TemplateView):
    template_name = 'panel.html'


class StatView(TemplateView):
    template_name = 'stats.html'


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'waiter.html'

    def get_queryset(self):
        return Order.objects.filter(employee=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'


class OrderNew(LoginRequiredMixin, CreateView):
    form_class = NewOrderForm
    model = Order
    template_name = 'order_new.html'

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)


class OrderEditView(LoginRequiredMixin, UpdateView):
    form_class = NewOrderForm
    model = Order
    template_name = 'order_edit.html'

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)


class OrderCloseView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'order_close.html'
    fields = ['is_open']

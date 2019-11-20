from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView

from arepo.models import Order


class HomePageView(TemplateView):
    template_name = 'home.html'


class PanelView(TemplateView):
    template_name = 'panel.html'


class StatView(TemplateView):
    template_name = 'stats.html'


class OrderListView(ListView):
    model = Order
    template_name = 'waiter.html'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'


class OrderNew(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'order_new.html'
    fields = ['table', 'dishes']

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)


class OrderEditView(UpdateView):
    model = Order
    template_name = 'order_edit.html'
    fields = ['table', 'tip', 'dishes', 'is_open']

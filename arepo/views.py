from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm, CheckboxSelectMultiple

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


class NewOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['table', 'dishes']
        widgets = {
            'dishes': CheckboxSelectMultiple()
        }


class OrderNew(LoginRequiredMixin, CreateView):
    form_class = NewOrderForm
    model = Order
    template_name = 'order_new.html'

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)


class OrderEditView(UpdateView):
    model = Order
    template_name = 'order_edit.html'
    fields = ['table', 'tip', 'dishes', 'is_open']

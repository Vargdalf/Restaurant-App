from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render

from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView

from arepo.forms import NewOrderForm
from arepo.models import Order, Dish, Employee


class HomePageView(TemplateView):
    template_name = 'home.html'


class PanelView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'panel.html'


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'waiter.html'

    def get_queryset(self):
        return Order.objects.filter(employee=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'


class OrderNewView(LoginRequiredMixin, CreateView):
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


class OrderCloseView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'order_close.html'
    fields = ['paid_amount', 'is_open']


class StatView(LoginRequiredMixin, TemplateView):
    template_name = 'stats.html'
    model = Order
    today = datetime.now().strftime('%d %b %Y')
    current_week = datetime.today().strftime('%W')
    list_of_dishes = Dish.objects.all()
    dish_counter = {}
    all_orders = Order.objects.all()

    def get(self, request, *args, **kwargs):
        """Tips stats"""
        waiter_orders = Order.objects.all().filter(employee__username=request.user.username, )
        today_orders = Order.objects.all().filter(employee__username=request.user.username, date=datetime.today(), )
        weekly_order = Order.objects.all().filter(employee__username=request.user.username,
                                                  date__week=datetime.today().strftime(
                                                      str((int(self.current_week) + 1))), )
        monthly_order = Order.objects.all().filter(employee__username=request.user.username,
                                                   date__month=datetime.today().strftime('%m'), )

        total_tips = waiter_orders.aggregate(Sum('tip'))['tip__sum']
        daily_tips = today_orders.aggregate(Sum('tip'))['tip__sum']
        weekly_tips = weekly_order.aggregate(Sum('tip'))['tip__sum']
        monthly_tips = monthly_order.aggregate(Sum('tip'))['tip__sum']

        """Order Stats"""
        for dish in self.list_of_dishes:
            self.dish_counter[dish.name] = ((dish.order_dishes.all().filter(
                employee__username=request.user.username).count()),
                                            dish.price * (dish.order_dishes.all().filter(
                                                employee__username=request.user.username).count()))

        # Total value of orders
        # if Order.is_open:
        total_value = []
        for price in self.dish_counter.values():
            total_value.append(price[1])
        total_value_of_orders = sum(total_value)


        # Achievements
        # ==================================================
        current_emp = Employee.objects.all().filter(username=f'{self.request.user.username}_user')[0]

        # Baby a triple
        if int(self.dish_counter['Coca-Cola'][0]) >= 3:
            current_emp.achievements.add(1)
        else:
            current_emp.achievements.remove(1)

        # Saving Cash
        if total_tips is not None:
            if total_tips >= 100:
                current_emp.achievements.add(2)
            else:
                current_emp.achievements.remove(2)
        else:
            current_emp.achievements.remove(2)

        achi_earned = current_emp.achievements.all()
        # =====================================================
        content = {'total_tips': total_tips, 'daily_tips': daily_tips, 'today': self.today,
                   'monthly_tips': monthly_tips, 'weekly_tips': weekly_tips,
                   'dish_counter': self.dish_counter,
                   'all_orders': self.all_orders, 'total_value_of_orders': total_value_of_orders,
                   'achi_earned': achi_earned}

        return render(request, self.template_name,
                      content, )

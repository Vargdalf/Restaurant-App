from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, Sum
from django.urls import reverse
from django.template.defaulttags import register


class Achievement(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(default=None)


class Employee(User):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='+')
    achievements = models.ManyToManyField(Achievement, blank=True)


class Dish(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Dishes'

    def __str__(self):
        return self.name


class Order(models.Model):
    table = models.IntegerField()
    employee = models.ForeignKey(User, on_delete=CASCADE)
    tip = models.IntegerField(default=0)
    dishes = models.ManyToManyField(Dish, related_name='order_dishes')
    date = models.DateField(auto_now_add=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f'Order for table no. {self.table}'

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])

    def get_full_price(self):
        try:
            full_price = Order.objects.get(pk=self.pk).dishes.aggregate(Sum('price'))['price__sum']
        except Order.DoesNotExist:
            full_price = None
        return full_price

    def get_all_tips(self):
        waiter_orders = Order.objects.all().filter(employee__username=self.employee)
        total_tips = waiter_orders.aggregate(Sum('tip'))['tip__sum']
        return total_tips

    def daily_tips(self):
        today_orders = Order.objects.all().filter(employee__username=self.employee, date=datetime.today())
        daily_tips = today_orders.aggregate(Sum('tip'))['tip__sum']
        return daily_tips

    def weekly_tips(self):
        current_week = datetime.today().strftime('%W')
        weekly_order = Order.objects.all().filter(employee__username=self.employee,
                                                  date__week=datetime.today().strftime(
                                                      str((int(current_week) + 1))))
        weekly_tips = weekly_order.aggregate(Sum('tip'))['tip__sum']
        return weekly_tips

    def monthly_tips(self):
        monthly_order = Order.objects.all().filter(employee__username=self.employee,
                                                   date__month=datetime.today().strftime('%m'))
        monthly_tips = monthly_order.aggregate(Sum('tip'))['tip__sum']
        return monthly_tips

    def dishes_sold(self):
        list_of_dishes = Dish.objects.all()
        dish_counter = {}
        for dish in list_of_dishes:
            if User.is_superuser:
                dish_counter[dish] = dish.order_dishes.all().count()
            else:
                dish_counter[dish] = dish.order_dishes.all().filter(employee__username=self.employee).count()
        return dish_counter

    def orders_value(self):
        total_value = None
        if User.is_superuser:
            all_orders = Order.objects.all()
        else:
            all_orders = Order.objects.all().filter(employee__username=self.employee)

        for order in all_orders:
            total_value += order.get_full_price()
        return total_value

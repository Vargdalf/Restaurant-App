from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, Sum
from django.urls import reverse


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
    paid_amount = models.IntegerField(default=0)
    dishes = models.ManyToManyField(Dish)
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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        self.tip = self.paid_amount - self.get_full_price()
        super(Order, self).save(*args, **kwargs)

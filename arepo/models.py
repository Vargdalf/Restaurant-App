from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, Sum
from django.urls import reverse


class Achievement(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(default=None)
    earned = models.BooleanField(default=False)

    def get_achivement(self):
        # Dish checker
        dish_counter = {}
        for dish in Order.objects.all():
            dish_counter[dish] = dish.order_dishes.all().filter(employee__username=User.username).count()
        # Tips checker
        total_tips = Order.objects.all().filter(employee__username=User.username).aggregate(Sum('tip'))['tip__sum']

        # Baby a tripple achivement
        if dish_counter['Cola'] >= 3:
            Achievement.objects.all()[0].earned = True
        else:
            Achievement.objects.all()[0].earned = False
        # Fir$t $avings achivement
        if total_tips >= 100:
            Achievement.objects.all()[1].earned = True
        else:
            Achievement.objects.all()[1].earned = False


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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        Achievement.get_achivement()
        try:
            self.tip = self.paid_amount - self.get_full_price()
        except TypeError:
            self.tip = 0
        super(Order, self).save(*args, **kwargs)

from django.contrib.auth.models import User
from django.db.models import Sum

from arepo.models import Order
from arepo.views import StatView


class BabyATripleAchievement:
    name = 'Baby a triple'
    key = 'triple'
    description = 'Sell a 3 cokes'
    bonus = 10.0
    dish_counter = StatView.dish_counter

    def evaluate(self, *args, **kwargs):
        if self.dish_counter['Cola'] >= 3:
            return True
        else:
            return False


class FirstSavingsAchievement:
    name = 'Fir$t $avings'
    key = 'savings'
    description = 'Earn 100 PLN in tips'
    bonus = 10.0
    waiter_orders = Order.objects.all().filter(employee__username=User.username)
    total_tips = waiter_orders.aggregate(Sum('tip'))['tip__sum']

    def evaluate(self, *args, **kwargs):
        if self.total_tips >= 100:
            return True
        else:
            return False

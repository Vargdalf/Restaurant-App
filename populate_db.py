import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant.settings")
django.setup()
from arepo.models import Dish, Achievement



def add_dishes_db():
    Dish.objects.create(name='Coca-Cola', description='Sprinkle sugar black water', price=5)
    Dish.objects.create(name='Pierogies', description='Fluffy with cheese', price=16)
    Dish.objects.create(name='Tea', description='Black as my heart', price=8)
    Dish.objects.create(name='Lasagne', description='Very tomato, very garfield', price=22)
    Dish.objects.create(name='Apple Tart', description='Triangle piece of tart with apples', price=12)

def add_achievements_db():
    Achievement.objects.create(name='Baby a triple', description='Sell 3 bottles of Coca-Cola')
    Achievement.objects.create(name='$aving Ca$h', description='Earn 100 PLN in tips')



if __name__ == '__main__':
    add_achievements_db()
    add_dishes_db()
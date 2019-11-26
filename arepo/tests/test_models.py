from django.test import TestCase

from model_bakery import baker

from arepo.models import Order, Dish


class DishModelTest(TestCase):
    def setUp(self):
        self.dish = baker.make(Dish)

    def test_string_representation(self):
        dish = Dish.objects.get(pk=1)
        self.assertEqual(str(dish), f'{dish.name}')


class OrderModelTest(TestCase):
    def setUp(self):
        self.dishes_set = baker.prepare(
            Dish,
            price=5,
            _quantity=2,
        )
        self.order = baker.make(
            Order,
            dishes=self.dishes_set,
        )
        self.order_without_dishes = baker.make(Order)

    def test_string_representation(self):
        order = Order.objects.get(pk=1)
        expected_result = f'Order for table no. {order.table}'
        self.assertEqual(str(order), expected_result)

    def test_get_absolute_url(self):
        order = Order.objects.get(pk=1)
        self.assertEqual(order.get_absolute_url(), '/waiter/order/1')

    def test_get_full_price(self):
        order = Order.objects.get(pk=1)
        empty_order = Order.objects.get(pk=2)
        self.assertEqual(order.get_full_price(), 10)
        self.assertEqual(empty_order.get_full_price(), 0)

    def test_save(self):
        # Order with dishes but without paid_amount
        order = Order.objects.get(pk=1)
        # Tip should equal as the order is still open
        self.assertEqual(order.tip, 0)
        # Simulationg the client paying including the tip
        order.paid_amount = 20
        order.save()
        # The tip should be more than 0
        self.assertEqual(order.tip, 10)

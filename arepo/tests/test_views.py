from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from arepo.models import Order


class HomePageViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accesible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')


class PanelViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('panel'))
        self.assertRedirects(response, '/accounts/login/?next=/panel/', target_status_code=404)

    def test_logged_in_uses_correct_template(self):
        self.login = self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('panel'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), f'{self.user.username}')
        self.assertTemplateUsed(response, 'panel.html')


class OrderListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')

        self.orders = baker.make(
            Order,
            employee=self.user,
            _quantity=5,
        )

        self.orders2 = baker.make(
            Order,
            employee=self.user2,
            _quantity=5,
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('waiter'))
        self.assertRedirects(response, '/accounts/login/?next=/waiter/', target_status_code=404)

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('waiter'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), f'{self.user.username}')
        self.assertTemplateUsed(response, 'waiter.html')

    def test_correct_orders_in_the_list(self):
        login = self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('waiter'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), f'{self.user.username}')
        self.assertTrue('order_list' in response.context)

        for order in response.context['order_list']:
            self.assertEqual(response.context['user'], order.employee)
            self.assertEqual(order.is_open, True)

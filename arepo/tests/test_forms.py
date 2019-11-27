from django.test import TestCase

from model_bakery import baker

from arepo.forms import NewOrderForm


class NewOrderFormTest(TestCase):

    def setUp(self):
        self.dishes = baker.make('Dish', _quantity=1)

    def test_NewOrder_form_valid(self):
        form = NewOrderForm(data={
            'table': 1,
            'dishes': self.dishes,
        })
        self.assertTrue(form.is_valid())

    def test_form_validation_for_blank_fields(self):
        form = NewOrderForm(data={
            'table': '',
            'dishes': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['table'], ['You need to assign a table'])
        self.assertEqual(form.errors['dishes'], ['You need to at least one dish'])

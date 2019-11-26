from django.test import TestCase

from arepo.forms import NewOrderForm


class NewOrderFormTest(TestCase):

    def test_form_validation_for_blank_fields(self):
        form = NewOrderForm(data={
            'table': '',
            'dishes': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['table'], ['You need to assign a table'])
        self.assertEqual(form.errors['dishes'], ['You need to at least one dish'])

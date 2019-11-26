from django.forms import ModelForm, CheckboxSelectMultiple

from arepo.models import Order


class NewOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['table', 'dishes']
        widgets = {
            'dishes': CheckboxSelectMultiple()
        }
        error_messages = {
            'table': {'required': 'You need to assign a table'},
            'dishes': {'required': 'You need to at least one dish'},
        }

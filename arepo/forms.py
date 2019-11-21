from django.forms import ModelForm, CheckboxSelectMultiple

from arepo.models import Order


class NewOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['table', 'dishes']
        widgets = {
            'dishes': CheckboxSelectMultiple()
        }

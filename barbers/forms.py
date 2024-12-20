from django import forms

from .models import Barber


class EditBarberProfileModelForm(forms.ModelForm):
    class Meta:
        model = Barber
        fields = ['name', 'shop_name', 'location', 'description']
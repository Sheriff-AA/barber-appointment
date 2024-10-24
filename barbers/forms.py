from django import forms

from .models import Barber


class BarberCreateModelForm(forms.ModelForm):
    class Meta:
        model = Barber
        fields = "__all__"
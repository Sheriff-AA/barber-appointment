from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from .models import Appointment, TimeSlot


class BookAppointmentForm(forms.ModelForm):
    slot_display = forms.CharField(disabled=True, required=False, label='Time Slot')

    class Meta:
        model = Appointment
        fields = ['customer_firstname', 'customer_lastname', 'customer_email', 'customer_phone_number', 'slot', 'slot_display']

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("slot_pk")
        super().__init__(*args, **kwargs)
        timeslot = TimeSlot.objects.get(pk=pk)
        self.fields['slot_display'].initial = str(timeslot)
        self.fields['slot'].widget = forms.HiddenInput()
        self.fields['slot'].initial = timeslot
        self.fields['customer_phone_number'].widget = forms.TextInput(attrs={'type': 'tel'})

    def clean(self):
        cleaned_data = super().clean()
        slot = cleaned_data.get('slot')
        if Appointment.objects.filter(slot=slot, is_accepted=True).exists():
            raise ValidationError("SORRY! This slot is already booked.")
        return cleaned_data

    def clean_customer_phone_number(self):
        phone_number = self.cleaned_data.get('customer_phone_number')
        if not phone_number.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return phone_number


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ["date", "start_time", "end_time", "is_reserved"]


class MultipleTimeslotForm(forms.Form):
    start_date = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={
                'type': 'date', 
                'class': 'datepicker'
            },
            time_attrs={
                'type': 'time', 
                'class': 'timepicker'
            },
        )
    )
    days_to_create = forms.IntegerField(min_value=1)
    slot_duration = forms.IntegerField(min_value=30, label='Slot duration (in mintes)')
    opening_hour = forms.TimeField(
        label='Opeing hour (08:00 AM)',
        widget=forms.TimeInput(
            attrs={
                'class': 'form-control',
                'type': 'time',
            }
        )
    )
    closing_hour = forms.TimeField(
        label='Closing hour (05:00 PM)',
        widget=forms.TimeInput(
            attrs={
                'type': 'time'
            }
        )
    )


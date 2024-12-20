from django import forms
from django.utils.timezone import now

from .models import Appointment, TimeSlot


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['slot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slot'].queryset = TimeSlot.objects.filter(
            appointments__isnull=True
        )  # Only show available time slots


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

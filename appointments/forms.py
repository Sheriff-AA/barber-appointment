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
    start_date = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget)
    days_to_create = forms.IntegerField()
    slot_duration = forms.IntegerField(label='Slot duration (in mintes)')
    opening_hour = forms.IntegerField()
    opening_minute = forms.IntegerField()
    closing_hour = forms.IntegerField()
    closing_minute = forms.IntegerField()

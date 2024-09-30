from django import forms
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

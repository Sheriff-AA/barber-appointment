from django.db import models
from datetime import timedelta

from profiles.models import UserProfile
from barbers.models import Barber
from utils.readable_date import formatted_date

RATINGS_CHOICES = (
    (1, "Bad!"),
    (2, "Meh"),
    (3, "Decent"),
    (4, "Barber cooked"),
    (5, "Give this man your money!")
)


class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_reserved = models.BooleanField(default=False)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('date', 'start_time', 'end_time', 'barber')

    def __str__(self):
        return f"{formatted_date(self.date)} from {self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')} with {self.barber}"
    

class Appointment(models.Model):
    customer_firstname = models.CharField(max_length=45, verbose_name='First Name')
    customer_lastname = models.CharField(max_length=45, verbose_name='Last Name')
    customer_email = models.EmailField(max_length=254, verbose_name='Email Address')
    customer_phone_number = models.CharField(max_length=20, verbose_name='Phone Number')
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='appointment', verbose_name='Time Slot')
    requested_on = models.DateTimeField(auto_now_add=True)
    accepted_on = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('customer_email', 'slot')

    def __str__(self):
        return f"Appointment with {self.customer_firstname} {self.customer_lastname} on {self.slot}"
    

class Rating(models.Model):
    value = models.IntegerField(choices=RATINGS_CHOICES, default=None, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

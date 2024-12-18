from django.db import models
from datetime import timedelta

from profiles.models import UserProfile
from barbers.models import Barber

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
        return f"{self.date} | {self.start_time} - {self.end_time}"
    

class Appointment(models.Model):
    customer_firstname = models.CharField(max_length=45)
    customer_lastname = models.CharField(max_length=45)
    customer_email = models.EmailField(max_length=254)
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='appointment')
    booked_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
# new field like requested_on ad accepted_on
    class Meta:
        unique_together = ('customer_email', 'slot')

    def __str__(self):
        return f"Appointment with {self.customer_firstname} {self.customer_lastname} on {self.slot}"
    

class Rating(models.Model):
    value = models.IntegerField(choices=RATINGS_CHOICES, default=None, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

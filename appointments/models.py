from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta


class User(AbstractUser):
    pass


class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        unique_together = ('date', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.date} | {self.start_time} - {self.end_time}"
    

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='appointments')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'slot')

    def __str__(self):
        return f"Appointment with {self.user.username} on {self.slot}"

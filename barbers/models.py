from django.db import models

from profiles.models import UserProfile

class Barber(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="barber")
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=220)

    def __str__(self):
        return f"{self.profile.user.username}"


class Comment(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)




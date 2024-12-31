from django.db import models
import uuid

from profiles.models import UserProfile

class Barber(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="barber")
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=220)
    name = models.CharField(max_length=50)
    shop_name = models.CharField(max_length=180)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.name} - {self.shop_name}"
    
    def save(self, *args, **kwargs):
        self.slug = f"{self.profile.user.username}".split('-')[1]
        super().save(*args, **kwargs)



class Comment(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
          primary_key=True, editable=False)




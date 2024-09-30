from django.contrib import admin
from .models import (User, Appointment, TimeSlot)

# Register your models here.
admin.site.register(User)
admin.site.register(Appointment)
admin.site.register(TimeSlot)

from django.contrib import admin

from .models import Barber, Comment
# Register your models here.

admin.site.register(Barber)
admin.site.register(Comment)
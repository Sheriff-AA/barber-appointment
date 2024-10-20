from django.contrib import admin


from .models import ProfileType, UserProfile
# Register your models here.

admin.site.register(ProfileType)
admin.site.register(UserProfile)

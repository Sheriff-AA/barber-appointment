from django.contrib import admin


from .models import ProfileType, UserProfile, User
# Register your models here.

admin.site.register(User)
admin.site.register(ProfileType)
admin.site.register(UserProfile)

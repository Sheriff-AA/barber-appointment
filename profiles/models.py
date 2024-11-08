from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings
from utils.generators import unique_username

User = settings.AUTH_USER_MODEL #appointments.User

ALLOW_CUSTOM_GROUPS = True
PROFILE_PERMISSIONS = settings.PROFILE_PERMISSIONS


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        new_slug = f"{self.email}".split('@')[0]
        unique_username(self, new_slug)
        super().save(*args, **kwargs)


class ProfileType(models.Model):
    name = models.CharField(max_length=120)
    groups = models.ManyToManyField(Group)
    permissions = models.OneToOneField(Permission,
        limit_choices_to={
            "content_type__app_label": "profiles","codename__in": [x[0] for x in PROFILE_PERMISSIONS]
            },
        on_delete=models.SET_NULL,
        null=True, blank=True
        )
    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        permissions = PROFILE_PERMISSIONS


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_type = models.ForeignKey(ProfileType, on_delete=models.CASCADE, verbose_name="Profile Type")


def user_profile_post_save(sender, instance, *args, **kwargs):
    user_profile_instance = instance
    user = user_profile_instance.user
    profiletype_obj = user_profile_instance.profile_type
    groups_ids = []
    if profiletype_obj is not None:
        groups = profiletype_obj.groups.all()
        groups_ids = groups.values_list('id', flat=True)

    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups_ids)
    else:
        profiletype_qs = ProfileType.objects.all()
        if profiletype_obj is not None:
            profiletype_qs = profiletype_qs.exclude(id=profiletype_obj.id)
        profiletype_groups = profiletype_qs.values_list("groups__id", flat=True)
        profiletype_groups_set = set(profiletype_groups) 
        current_groups = user.groups.all().values_list('id', flat=True)
        groups_ids_set = set(groups_ids)
        current_groups_set = set(current_groups) - profiletype_groups_set
        final_group_ids = list(groups_ids_set | current_groups_set)
        user.groups.set(final_group_ids)


post_save.connect(user_profile_post_save, sender=UserProfile)
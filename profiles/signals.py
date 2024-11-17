from allauth.account.signals import email_confirmed, user_signed_up
from django.dispatch import receiver
import secrets
from django.contrib.auth import get_user_model

from utils.profile_types import barber_profiletype
from .models import UserProfile
from barbers.models import Barber


@receiver(email_confirmed)
def handle_email_confirmation_(request, email_address, **kwargs):
    user = email_address.user

    # Set the username and save the user if needed
    if not user.username:
        user.username = user.email
        user.set_password(secrets.token_urlsafe(13))
    user.is_active = True
    user.save()

    # Create or get the user profile
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        profile_type=barber_profiletype
    )

    # Create Barber object if profile was just created
    if created:
        Barber.objects.create(
            profile=profile,
            description="No description...",
            location="None",
            name=f"{profile.user.username}",
            shop_name=f"{profile.user.username}'s Shop",
            slug = f"{profile.user.username}".split('-')[1]
        )


@receiver(user_signed_up)
def handle_user_signup_(request, user, **kwargs):
    # user.is_active = False
    user.save()
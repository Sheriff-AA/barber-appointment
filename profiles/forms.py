from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.conf import settings
import secrets

from utils.password_gen import password_gen
from utils.profile_types import barber_profiletype
from .models import UserProfile
from barbers.models import Barber

User = settings.AUTH_USER_MODEL


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password1')
        self.fields.pop('password2')

    def save(self, request):
        user = super().save(request)
        user.set_password(secrets.token_urlsafe(13))
        user.username = user.email
        user.save()

        return user


class CustomSocialSignupForm(SocialSignupForm):
    def save(self, request):
        user = super().save(request)
        return user
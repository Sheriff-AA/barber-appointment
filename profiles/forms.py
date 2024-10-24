from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.conf import settings
import secrets

from utils import password_gen

User = settings.AUTH_USER_MODEL


class CustomSignupForm(SignupForm):
    # email = forms.EmailField()

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
        return super().save(request)
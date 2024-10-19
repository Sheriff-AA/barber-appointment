from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from appointments.views import LandingPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name="landing-page"),
    path("appointments/", include("appointments.urls", namespace="appointments")),
    path('accounts/', include('allauth.urls')),
]

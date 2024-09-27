from django.urls import path, include

from .views import (AppointmentListAPIView,
                   )

"""
BASE ENDPOINT /api
"""
app_name = "api"


urlpatterns = [
    path("", AppointmentListAPIView.as_view(), name="appointment_list")

]


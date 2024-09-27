from django.urls import path, include

from .views import (AppointmentListAPIView,
                    TimeSlotListAPIView,
                   )

"""
BASE ENDPOINT /api
"""
app_name = "api"


urlpatterns = [
    path("appointments/", AppointmentListAPIView.as_view(), name="appointment_list"),
    path("timeslots/", TimeSlotListAPIView.as_view(), name="timeslot_list"),
]


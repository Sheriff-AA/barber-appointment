from rest_framework import generics


from appointments.models import Appointment
from .serializers import AppointmentSerializer


class AppointmentListAPIView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
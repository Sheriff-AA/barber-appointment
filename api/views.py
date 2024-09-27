from rest_framework import generics


from appointments.models import Appointment, TimeSlot
from .serializers import AppointmentSerializer, TimeSlotSerializer


class AppointmentListAPIView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class TimeSlotListAPIView(generics.ListAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
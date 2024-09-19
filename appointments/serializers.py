from rest_framework import serializers
from .models import TimeSlot, Appointment


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    slot = TimeSlotSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'

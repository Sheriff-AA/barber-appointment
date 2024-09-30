from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import TimeSlot, Appointment
from .forms import AppointmentForm


def index(request):
    return render(request, 'landing_page.html')


class AppointmentsListView(generic.ListView):
    template_name = "appointments/appointments_list"


class AvailableTimeSlotsView(generic.ListView):
    model = TimeSlot
    template_name = 'appointments/available_slots.html'
    context_object_name = 'time_slots'

    def get_queryset(self):
        # Filter time slots that are not booked and are in the future
        return TimeSlot.objects.filter(appointments__isnull=True).order_by('date', 'start_time')


class BookAppointmentView(LoginRequiredMixin, generic.CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/book_appointment.html'
    success_url = reverse_lazy('appointment_success')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user to the logged-in user
        slot = form.cleaned_data['slot']
        
        # Check if the time slot is already booked
        if Appointment.objects.filter(slot=slot).exists():
            form.add_error('slot', 'This time slot is already booked.')
            return self.form_invalid(form)
        
        return super().form_valid(form)
    

class UserAppointmentsView(LoginRequiredMixin, generic.ListView):
    model = Appointment
    template_name = 'appointments/user_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        # Only show appointments for the logged-in user
        return Appointment.objects.filter(user=self.request.user).order_by('slot__date', 'slot__start_time')

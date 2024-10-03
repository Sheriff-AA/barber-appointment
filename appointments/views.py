from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from django.utils.timezone import now
from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin


from .models import TimeSlot, Appointment
from .forms import AppointmentForm


def index(request):
    return render(request, 'landing_page.html')


class AppointmentsListView(generic.ListView):
    template_name = "appointments/appointments_list"
    context_object_name = 'appointments'

    def get_queryset(self):
        # Filter time slots that are not booked and are in the future
        return Appointment.objects.all().order_by('date', 'start_time')


def event_list(request):
    events = TimeSlot.objects.all()
    events_data = []
    for event in events:
        events_data.append({
            'title': event.date,
            'start': event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'allDay': False,
        })
    return JsonResponse(events_data, safe=False)


class AvailableTimeSlotsView(generic.ListView):
    model = TimeSlot
    template_name = 'appointments/available_slots.html'
    context_object_name = 'time_slots'

    def get_queryset(self):
        # Filter time slots that are not booked and are in the future
        return TimeSlot.objects.filter(appointments__isnull=True).filter(date__gt=now().date()).order_by('date', 'start_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        time_slots = self.get_queryset()

        # Group time slots by date
        grouped_slots = defaultdict(list)
        for slot in time_slots:
            grouped_slots[slot.date].append(slot)
        # print(grouped_slots.items())

        context['time_slots_by_date'] = sorted(grouped_slots.items())
        return context


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

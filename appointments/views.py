from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.timezone import now
from datetime import timedelta, datetime
from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.mixins import barber_required, BarberRequiredMixin

from .models import TimeSlot, Appointment
from barbers.models import Barber
from utils.create_multiple_timeslots import create_timeslots
from .forms import (
    RequestAppointmentForm, 
    MultipleTimeslotForm, 
    SingleTimeslotForm
)


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


class AppointmentPageView(generic.TemplateView):
    template_name = 'appointments/appointments_list.html'


class AppointmentsListView(generic.ListView):
    template_name = "appointments/appointments_list.html"
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
        return TimeSlot.objects.filter(date__gt=now().date()).order_by('date', 'start_time')
    
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


class RequestAppointmentCreateView(generic.CreateView):
    model = Appointment
    form_class = RequestAppointmentForm
    template_name = 'appointments/request_appointment.html'
    success_url = reverse_lazy('appointments:appointment_success')

    def get_form_kwargs(self, **kwargs):
        kwargs = super(RequestAppointmentCreateView, self).get_form_kwargs(**kwargs)
        kwargs.update({'slot_pk': self.kwargs['slug']})
        return kwargs

    def form_valid(self, form):
        slot = form.cleaned_data['slot']
        customer_firstname = form.cleaned_data['customer_firstname']
        customer_lastname = form.cleaned_data['customer_lastname']
        customer_email = form.cleaned_data['customer_email']
        customer_phone_number = form.cleaned_data['customer_phone_number']
        
        # # Check if the time slot is already booked
        # if Appointment.objects.filter(slot=slot).exists():
        #     form.add_error('slot', 'This time slot is already booked.')
        #     return self.form_invalid(form)
        
        return super().form_valid(form)
    

class UserAppointmentsView(LoginRequiredMixin, generic.ListView):
    model = Appointment
    template_name = 'appointments/user_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        # Only show appointments for the logged-in user
        return Appointment.objects.filter(user=self.request.user).order_by('slot__date', 'slot__start_time')


@barber_required
def create_multiple_timeslots(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = MultipleTimeslotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            days_to_create = form.cleaned_data['days_to_create']
            slot_duration = form.cleaned_data['slot_duration']
            opening_hour = form.cleaned_data['opening_hour']
            closing_hour = form.cleaned_data['closing_hour']
            barber_user = Barber.objects.get(profile=request.user.profile)

            if opening_hour < closing_hour:
                create_timeslots(
                    start_date=start_date,
                    days_to_create=days_to_create,
                    duration=slot_duration,
                    opening_hour=opening_hour,
                    closing_hour=closing_hour,
                    barber_user=barber_user
                )
            else:
                # pass specific error to form or do it in forms
                return render(request, "appointments/barber_create_multiple_timeslots.html", {"form": form})
            return HttpResponseRedirect("success/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MultipleTimeslotForm()

    return render(request, "appointments/barber_create_multiple_timeslots.html", {"form": form})


@barber_required
def create_single_timeslots(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SingleTimeslotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            slot_date = form.cleaned_data['slot_date']
            days_to_create = 1
            slot_duration = form.cleaned_data['slot_duration']
            starting_time = form.cleaned_data['starting_time']

            duration = timedelta(minutes=slot_duration)
            closing_time = (datetime.combine(slot_date, starting_time) + duration).time()
            barber_user = Barber.objects.get(profile=request.user.profile)

            if starting_time < closing_time:
                create_timeslots(
                    start_date=slot_date,
                    days_to_create=days_to_create,
                    duration=slot_duration,
                    opening_hour=starting_time,
                    closing_hour=closing_time,
                    barber_user=barber_user
                )
            else:
                # pass specific error to form or do it in forms
                return render(request, "appointments/barber_create_single_timeslots.html", {"form": form})
            return HttpResponseRedirect("success/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SingleTimeslotForm()

    return render(request, "appointments/barber_create_single_timeslots.html", {"form": form})



class BarberAppointmentDeleteView(BarberRequiredMixin, generic.TemplateView):
    template_name = "appointments/partials/modals/reject_appointment.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)        
        context.update({
            'appointment': get_object_or_404(Appointment, slug=context['slug'])
        }) 
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, slug=kwargs['slug'])
        appointment.delete()
        return render(request, "appointments/partials/modals/success_appointment.html")
    

class BarberAppointmentAcceptView(BarberRequiredMixin, generic.TemplateView):
    template_name = "appointments/partials/modals/accept_appointment.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)        
        context.update({
            'appointment': get_object_or_404(Appointment, slug=context['slug'])
        }) 
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, slug=kwargs['slug'])
        appointment.is_accepted = True
        appointment.slot.is_reserved = True
        appointment.accepted_on = now()
        appointment.save()

        Appointment.objects.filter(slot=appointment.slot).exclude(slug=appointment.slug).delete()

        return render(request, "appointments/partials/modals/success_appointment.html")

    
class BarberAppointmentReadDetailView(generic.TemplateView):
    template_name = "appointments/partials/modals/read_appointment_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'appointment': get_object_or_404(Appointment, slug=context['slug'])
        })
        return context


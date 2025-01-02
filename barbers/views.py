from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic
from django.utils.timezone import now
from collections import defaultdict

from .forms import EditBarberProfileModelForm
from .models import Barber
from profiles.mixins import BarberRequiredMixin
from appointments.models import TimeSlot, Appointment


class BarberProfileUpdateView(BarberRequiredMixin, generic.UpdateView):
    template_name = "barbers/barber_profile_edit.html"
    form_class = EditBarberProfileModelForm

    def get_queryset(self):
        return Barber.objects.all()

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("barbers:barber-profile", kwargs={'slug': self.get_object().slug })
    

class BarberListView(generic.ListView):
    template_name = "barbers/list_barbers.html"
    model = Barber
    context_object_name = 'barbers'


class BarberDetailView(generic.DetailView):
    template_name = "barbers/detail_barbers.html"
    context_object_name = 'barber'

    def get_queryset(self):
        return Barber.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        available_slots = TimeSlot.objects.filter(
            barber=self.get_object()).filter(
            is_reserved=False).order_by('date', 'start_time')

        # grouped_slots = defaultdict(list)
        # for slot in available_slots:
        #     grouped_slots[slot.date].append(slot)

        context.update({
            'slots': available_slots,
        })

        return context


class BarberProfileDetailView(BarberRequiredMixin, generic.DetailView):
    template_name = "barbers/barber_profile.html"
    context_object_name = 'barber'

    def get_queryset(self):
        return Barber.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        available_slots = TimeSlot.objects.filter(
            barber=self.get_object()).filter(
            date__lt=now().date()).filter(
            is_reserved=False).order_by('date', 'start_time')
        appointments = Appointment.objects.filter(slot__barber=self.get_object())

        # Group time slots by date
        # grouped_slots = defaultdict(list)
        # for slot in available_slots:
        #     grouped_slots[slot.date].append(slot)
        
        context.update({
            'slots': available_slots,
            'requested_appointments': appointments.filter(is_accepted=False),
            'confirmed_appointments': appointments.filter(is_accepted=True)
        })

        return context
    

class BarbersTimeslotListTemplateView(generic.TemplateView):
    template_name = "barbers/partials/barber_timeslots.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        barber = get_object_or_404(Barber, slug=context['slug'])
        available_slots = TimeSlot.objects.filter(
            barber=barber).filter(
            is_reserved=False).order_by('date', 'start_time')
        
        context.update({
            'slots': available_slots,
            'barber': barber
        })
        
        if request.user.is_authenticated and request.user.has_perm('profiles.access_to_barber_actions'):
            context.update({
                'is_barber': True
            })
            
        return render(request, self.template_name, context)
    


from django.urls import path
from django.views.generic import TemplateView


from .views import (
    AppointmentPageView, 
    AvailableTimeSlotsView, 
    RequestAppointmentCreateView, 
    UserAppointmentsView, 
    AppointmentsListView, 
    CreateBarberTimeSlotsView,
    BarberAppointmentDeleteView,
    BarberAppointmentAcceptView,
    BarberAppointmentReadDetailView,
    event_list, 
    create_multiple_timeslots
)

"""
BASE ENDPOINT /appointments
"""
app_name = "appointments"


urlpatterns = [
    path('', AppointmentPageView.as_view(), name='index'),
    path('available-slots/', AvailableTimeSlotsView.as_view(), name='available_slots'),
    path('book/slot-<slug:slug>/', RequestAppointmentCreateView.as_view(), name='request_appointment'),
    path('my-appointments/', UserAppointmentsView.as_view(), name='user_appointments'),
    path('all-appointments/', AppointmentsListView.as_view(), name='list_appointments'),

    path('success/', TemplateView.as_view(template_name='appointments/success.html'), name='appointment_success'),
    path('create-timeslots', CreateBarberTimeSlotsView.as_view(), name='create_timeslots'),
    path('create-bulk-timeslots', create_multiple_timeslots, name='create_multiple_timeslots'),
    path('events/json/', event_list, name='event_list'),  # Event JSON data

    path('<slug:slug>/delete', BarberAppointmentDeleteView.as_view(), name='reject-appointment'),
    path('<slug:slug>/accept', BarberAppointmentAcceptView.as_view(), name='accept-appointment'),
    path('<slug:slug>/details', BarberAppointmentReadDetailView.as_view(), name='read-appointment-detail'),
]
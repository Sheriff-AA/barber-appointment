from django.urls import path
from django.views.generic import TemplateView


from .views import AppointmentPageView, AvailableTimeSlotsView, BookAppointmentView, UserAppointmentsView, AppointmentsListView, CreateBarberTimeSlotsView, event_list, create_multiple_timeslots

"""
BASE ENDPOINT /appointments
"""
app_name = "appointments"


urlpatterns = [
    path('', AppointmentPageView.as_view(), name='index'),
    path('available-slots/', AvailableTimeSlotsView.as_view(), name='available_slots'),
    path('book/slot-<int:pk>/', BookAppointmentView.as_view(), name='book_appointment'),
    path('my-appointments/', UserAppointmentsView.as_view(), name='user_appointments'),
    path('all-appointments/', AppointmentsListView.as_view(), name='list_appointments'),
    path('success/', TemplateView.as_view(template_name='appointments/success.html'), name='appointment_success'),
    path('create-timeslots', CreateBarberTimeSlotsView.as_view(), name='create_timeslots'),
    path('create-bulk-timeslots', create_multiple_timeslots, name='create_multiple_timeslots'),
    path('events/json/', event_list, name='event_list'),  # Event JSON data
]
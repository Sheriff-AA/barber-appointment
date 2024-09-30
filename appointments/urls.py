from django.urls import path
from django.views.generic import TemplateView


from .views import index, AvailableTimeSlotsView, BookAppointmentView, UserAppointmentsView, AppointmentsListView

"""
BASE ENDPOINT /appointments
"""
app_name = "appointments"


urlpatterns = [
    path('', index, name='index'),
    path('available-slots/', AvailableTimeSlotsView.as_view(), name='available_slots'),
    path('book/', BookAppointmentView.as_view(), name='book_appointment'),
    path('my-appointments/', UserAppointmentsView.as_view(), name='user_appointments'),
    path('all-appointments/', AppointmentsListView.as_view(), name='list_appointments'),
    path('appointment-success/', TemplateView.as_view(template_name='appointments/success.html'), name='appointment_success'),
]
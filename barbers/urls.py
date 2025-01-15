from django.urls import path
from django.views.generic import TemplateView

from .views import (
    BarberProfileDetailView, 
    BarberListView, 
    BarberDetailView, 
    BarberProfileUpdateView, 
    BarbersTimeslotListTemplateView, 
    BarberTimeslotDeleteView,
    BarbersAppointmentRequestListTemplateView,
    BarbersAppointmentConfirmedListTemplateView,
)

"""
BASE ENDPOINT /barbers
"""
app_name = "barbers"


urlpatterns = [
    path('', BarberListView.as_view(), name='list-barber'),
    path('book/', TemplateView.as_view(template_name='barbers/book_barber_slots.html'), name='book-barber'),
    path('requests/', TemplateView.as_view(template_name='barbers/barber_appointment_requests.html'), name='barber-appointment-requests'),

    path('<slug:slug>/edit/', BarberProfileUpdateView.as_view(), name='edit-barber-profile'),
    path('<slug:slug>/details', BarberDetailView.as_view(), name='detail-barber'),
    path('<slug:slug>/profile', BarberProfileDetailView.as_view(), name='barber-profile'),

    path('<slug:slug>/timeslots', BarbersTimeslotListTemplateView.as_view(), name='barber-timeslots'),
    path('<slug:slug>/confirmed', BarbersAppointmentConfirmedListTemplateView.as_view(), name='barber-confirmed'),
    path('<slug:slug>/requests', BarbersAppointmentRequestListTemplateView.as_view(), name='barber-requests'),
    path('<slug:slug>/delete-timeslots', BarberTimeslotDeleteView.as_view(), name='delete-timeslots'),
    
]
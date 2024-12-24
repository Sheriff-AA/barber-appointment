from django.urls import path
from django.views.generic import TemplateView

from .views import EditBarberProfileView, BarberListView, BarberDetailView, BarberProfileView

"""
BASE ENDPOINT /barbers
"""
app_name = "barbers"


urlpatterns = [
    path('', BarberListView.as_view(), name='list-barber'),
    path('book/', TemplateView.as_view(template_name='barbers/book_barber_slots.html'), name='book-barber'),
    path('requests/', TemplateView.as_view(template_name='barbers/barber_requests.html'), name='barber-appointment-requests'),
    path('<slug:slug>/edit/', EditBarberProfileView.as_view(), name='edit-barber-profile'),
    path('<slug:slug>/details', BarberDetailView.as_view(), name='detail-barber'),
    path('<slug:slug>/profile', BarberProfileView.as_view(), name='barber-profile'),
]
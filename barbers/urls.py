from django.urls import path

from .views import EditBarberProfileView, BarberListView, BarberDetailView, BarberProfileView

"""
BASE ENDPOINT /barbers
"""
app_name = "barbers"


urlpatterns = [
    path('', BarberListView.as_view(), name='list-barber'),
    path('<slug:slug>/edit/', EditBarberProfileView.as_view(), name='edit-barber-profile'),
    path('<slug:slug>/details', BarberDetailView.as_view(), name='detail-barber'),
    path('<slug:slug>/profile', BarberProfileView.as_view(), name='barber-profile'),
]
from django.urls import path

from .views import CreateBarberView, BarberListView, BarberDetailView

"""
BASE ENDPOINT /barbers
"""
app_name = "barbers"


urlpatterns = [
    path('create/', CreateBarberView.as_view(), name='create-barber'),
    path('', BarberListView.as_view(), name='list-barber'),
    path('<slug:slug>/', BarberDetailView.as_view(), name='detail-barber'),
]
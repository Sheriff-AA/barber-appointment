from django.urls import path

from .views import index

"""
BASE ENDPOINT /appointments
"""
app_name = "appointments"


urlpatterns = [
    path('', index, name='index')
]
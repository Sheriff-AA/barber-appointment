from django.shortcuts import render
from django.views import generic


# Create your views here.
def index(request):
    return render(request, 'landing_page.html')


class AppointmentsListView(generic.ListView):
    template_name = "appointments/appointments_list"
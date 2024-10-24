from django.shortcuts import render, reverse
from django.views import generic

from .forms import BarberCreateModelForm
from .models import Barber

class CreateBarberView(generic.CreateView):
    template_name = "barbers/create_barber.html"
    form_class = BarberCreateModelForm
    success_url = reverse('list-barber')

    def form_valid(self, form):
        return super().form_valid(form)
    

class BarberListView(generic.ListView):
    template_name = "barbers/list_barber.html"
    model = Barber
    context_object_name = 'barbers'
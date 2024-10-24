from django.shortcuts import render, reverse
from django.views import generic

from .forms import BarberCreateModelForm
from .models import Barber

class CreateBarberView(generic.CreateView):
    template_name = "barbers/create_barber.html"
    form_class = BarberCreateModelForm

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("barbers:list-barbers")
    

class BarberListView(generic.ListView):
    template_name = "barbers/list_barbers.html"
    model = Barber
    context_object_name = 'barbers'
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Plant, Entry
from django.contrib import messages
# from django.http import HttpResponse

def home(request):
    context = {
        'plants': Plant.objects.all()
    }
    return render(request, 'journal/home.html', context)

class PlantListView(ListView):
    model = Plant
    template_name = 'journal/home.html'
    context_object_name = 'plants'
    ordering = ['location', 'name']

class PlantDetailView(DetailView):
    model = Plant

class PlantCreateView(LoginRequiredMixin, CreateView):
    model = Plant
    fields = ['name', 'image', 'location', 'bought', 'schedule']
    def form_valid(self, form): # override parent form validation to set plant owner to current user automatically
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PlantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Plant
    fields = ['name', 'image', 'location', 'bought', 'schedule']
    def form_valid(self, form): # override parent form validation to set plant owner to current user automatically
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self): # make sure that person trying to update a plant is the owner of that plant
        plant = self.get_object()
        if self.request.user == plant.owner:
            return True
        return False

class PlantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Plant

    def test_func(self): # make sure that person trying to update a plant is the owner of that plant
        plant = self.get_object()
        if self.request.user == plant.owner:
            return True
        return False
    
    success_url = '/' # bring us back to the home page
    success_message = 'Your plant was successfully deleted.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PlantDeleteView, self).delete(request, *args, **kwargs)
    

def about(request):
    return render(request, 'journal/about.html', {'title':'About'})

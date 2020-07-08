from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Plant, Entry
from django.contrib import messages
# from django.http import HttpResponse
from .forms import EntryCreateForm

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
    

class EntryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = EntryCreateForm
    model = Entry
    #fields = ['plant', 'note', 'watered', 'fertilized', 'repotted', 'treated']
    
    def get_initial(self):
        plant = Plant.objects.get(pk=self.kwargs['pk'])
        return {'plant': plant}
    
    def test_func(self): # make sure that person trying to update a plant is the owner of that plant
        entry = self.get_object()
        if self.request.user == entry.plant.owner:
            return True
        return False

    '''def form_valid(self, form): # override parent form validation to set plant owner to current user automatically
        form.instance.owner = self.request.user
        return super().form_valid(form)'''


from django.shortcuts import render

def error_403(request, exception):
        data = {}
        return render(request,'journal/403.html', data)

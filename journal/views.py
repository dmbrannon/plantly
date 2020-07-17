from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import FormMixin, FormView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from .forms import EntryCreateForm, EntryWaterForm, PlantCreateForm
from .models import Plant, Entry

def about(request):
    """ Show about page explaining app purpose. """
    return render(request, 'journal/about.html', {'title': 'About'})

class PlantListView(ListView):
    """ List all of user's plants on home page if they are logged in. """
    model = Plant
    template_name = 'journal/home.html'
    context_object_name = 'plants'
    ordering = ['location', 'name']
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(owner=self.request.user).order_by('location', 'name')
        else:
            dana = User.objects.filter(username='dana').first()
            return super().get_queryset().filter(owner=dana)

class PlantDetailView(FormMixin, DetailView):
    """ Show details of plant and handle 'Water Me!' button submission. """
    model = Plant
    form_class = EntryWaterForm

    def get_success_url(self):
        return reverse('plant-detail', kwargs={'pk': self.object.id})

    # If Water Me! button is pressed, update plant last_watered and return to home page with success
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        messages.success(request, f'Your {self.object.name} has been watered!')
        self.object.last_watered = timezone.now()
        self.object.save()
        # note = "Watered after " + str((timezone.now() - self.object.last_watered).days) + " days"
        # Entry.objects.create(plant=self.object, note=note, date_created=timezone.now(), watered='Y', fertilized='N', repotted='N', treated='N')
        return redirect('journal-home')

class PlantCreateView(LoginRequiredMixin, CreateView):
    """ Create a plant and set the owner and cropping fields automatically. """
    model = Plant
    form_class = PlantCreateForm
    #fields = ['name', 'image', 'location', 'bought', 'schedule']
    def form_valid(self, form): # override parent form validation to set plant owner to current user automatically
        form.instance.owner = self.request.user
        plant = form.save()
        if plant.image.height > plant.image.width:
            form.instance.cropping = f'0,0,{plant.image.width},{plant.image.width}'
        else:
            form.instance.cropping = f'0,0,{plant.image.height},{plant.image.height}'
        return super().form_valid(form)



class PlantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Update plant if user is the plant owner and auto set the cropping field again. """
    model = Plant
    form_class = PlantCreateForm
    #fields = ['name', 'image', 'location', 'bought', 'schedule']
    def form_valid(self, form): # override parent form validation to set plant owner to current user automatically
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self): # make sure that person trying to update a plant is the owner of that plant
        plant = self.get_object()
        if self.request.user == plant.owner:
            return True
        return False

    def post(self, request, **kwargs):
        plant = self.get_object()
        request.POST = request.POST.copy()
        if plant.image.height > plant.image.width:
            request.POST['cropping'] = f'0,0,{plant.image.width},{plant.image.width}'
        else:
            request.POST['cropping'] = f'0,0,{plant.image.height},{plant.image.height}'
        return super(PlantUpdateView, self).post(request, **kwargs)

class PlantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Delete a plant if user is plant owner and redirect to home page with message. """
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
    """ Create a journal entry with auto-populated plant field. """
    form_class = EntryCreateForm
    model = Entry

    # Redirect to plant detail view after journal entry created
    def get_success_url(self):
        return reverse('plant-detail', kwargs={'pk': self.kwargs.get('pk')})

    # Pass the plant into the view so it can be accessed
    def form_valid(self, form):
        form.instance.plant = Plant.objects.get(id=self.kwargs.get('pk'))    
        return super(EntryCreateView, self).form_valid(form)

    def get_initial(self):
        plant = Plant.objects.get(pk=self.kwargs['pk'])
        return {'plant': plant}

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView, self).get_context_data(**kwargs)
        context['plant'] = Plant.objects.get(pk=self.kwargs['pk'])
        return context

    def test_func(self): # make sure that person trying to update a plant is the owner of that plant
        if self.request.user == Plant.objects.get(pk=self.kwargs['pk']).owner:
            return True
        return False

def error_403(request, exception):
    """ Show custom 403 error page. """
    data = {}
    return render(request,'journal/403.html', data)

def error_404(request, exception):
    """ Show custom 404 error page. """
    data = {}
    return render(request,'journal/404.html', data)

def error_500(request, exception):
    """ Show custom 500 error page. """
    data = {}
    return render(request,'journal/500.html', data)

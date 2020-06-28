from django.shortcuts import render
from .models import Plant, Entry
# from django.http import HttpResponse

def home(request):
    context = {
        'plants': Plant.objects.all()
    }
    return render(request, 'journal/home.html', context)

def about(request):
    return render(request, 'journal/about.html', {'title':'About'})

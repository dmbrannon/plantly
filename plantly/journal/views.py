from django.shortcuts import render
from .models import Plant, Entry
# from django.http import HttpResponse

plants = [
    {
        'name':'Bird of Paradise',
        'location':'Kitchen',
        'last_watered':'11/01/2020',
        'last_fertilized':'11/3/2020',
        'bought':'10/31/2020',
        'notes':'Leaf yellowed',
        'id':'01'
    },
    {
        'name':'Snake Plant',
        'location':'Bedroom',
        'last_watered':'12/01/2020',
        'last_fertilized':'12/3/2020',
        'bought':'11/29/2020',
        'notes':'Repotted',
        'id':'02'
    },
]

def home(request):
    context = {
        'plants': Plant.objects.all()
    }
    return render(request, 'journal/home.html', context)

def about(request):
    return render(request, 'journal/about.html', {'title':'About'})

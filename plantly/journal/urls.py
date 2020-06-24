from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='journal-home'),
    # we will do reverse lookups on this route so we don't want to name it 
    # something generic like home cuz then it will collide with other apps
    path('about/', views.about, name='journal-about'),
]
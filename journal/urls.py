from django.urls import path
from . import views
from .views import PlantListView, PlantDetailView, PlantCreateView, PlantUpdateView, PlantDeleteView, EntryCreateView

urlpatterns = [
    path('', PlantListView.as_view(), name='journal-home'),
    # we will do reverse lookups on this route so we don't want to name it 
    # something generic like home cuz then it will collide with other apps
    path('plant/<int:pk>/', PlantDetailView.as_view(), name='plant-detail'),
    path('plant/<int:pk>/update/', PlantUpdateView.as_view(), name='plant-update'),
    path('plant/<int:pk>/delete/', PlantDeleteView.as_view(), name='plant-delete'),
    path('plant/new/', PlantCreateView.as_view(), name='plant-create'),
    path('plant/<int:pk>/entry/new/', EntryCreateView.as_view(), name='entry-create'),
]
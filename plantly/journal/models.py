from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename): 
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

#https://www.geeksforgeeks.org/imagefield-django-models/
class Plant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    bought = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to=user_directory_path)
    schedule = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True) #date only when created, cant update this
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} {self.id}"

class Entry(models.Model):
    YES_NO_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    note = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    watered = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')
    fertilized = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')
    repotted = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')
    treated = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')
    
    def __str__(self):
        return f"{self.note}"
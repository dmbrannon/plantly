import os

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
from image_cropping.fields import ImageRatioField
from PIL import Image, ExifTags

def user_directory_path(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

#https://www.geeksforgeeks.org/imagefield-django-models/
class Plant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    bought = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', blank=True, upload_to=user_directory_path)
    # size is "width x height"
    cropping = ImageRatioField('image', '300x300')

    schedule = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True) # date only when created, cant update this
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    last_watered = models.DateTimeField(default=timezone.now)

    # Make user file uploads smaller, fix crop
    def save(self, *args, **kwargs):
        self.cropping = '0,0,300,300'

        super().save(*args, **kwargs) # call parent class to save image first
        img = Image.open(self.image.path) # open this Profile instance's image

        try:
            image = Image.open(self.image.path)

            for orientation in ExifTags.TAGS.keys():
                #print(ExifTags.TAGS.keys()):
                if ExifTags.TAGS[orientation]=='Orientation':
                    break

            exif = dict(image._getexif().items())

            if exif[orientation] == 3:
                image=image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image=image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image=image.rotate(90, expand=True)

            image.save(self.image.path)
            image.close()
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass

        if img.height > 300 or img.width > 300:
            if img.height > img.width:
                output_size = (300, int(img.height/(img.width/300)))
                img.thumbnail(output_size)
                img.save(self.image.path) # overwrite the large image
            else:
                output_size = (int(img.width/(img.height/300)), 300)
                img.thumbnail(output_size)
                img.save(self.image.path) # overwrite the large image

    @property
    def is_due(self):
        return (timezone.now() - self.last_watered).days == self.schedule

    @property
    def is_past_due(self):
        return (timezone.now() - self.last_watered).days > self.schedule

    @property
    def watered_today(self):
        return (timezone.now() - self.last_watered).seconds/60/60 < 16 and (timezone.now() - self.last_watered).days < 1

    def __str__(self):
        return f"{self.name} {self.id}"

    def get_absolute_url(self):
        return reverse('plant-detail', kwargs={'pk': self.pk})

class Entry(models.Model):
    YES_NO_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    note = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    watered = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')
    fertilized = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')
    repotted = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')
    treated = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')

    def __str__(self):
        return f"{self.plant.name} {self.plant.id}: {self.note}"
    
    # Tell django where to go after creation of a new Entry
    def get_absolute_url(self):
        return reverse('plant-detail', kwargs={'pk': self.plant.pk})



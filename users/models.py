from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}\'s Profile'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # call parent class to save image first
        img = Image.open(self.image.path) # open this Profile instance's image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path) # overwrite the large image
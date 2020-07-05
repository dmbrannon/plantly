from django.db.models.signals import post_save
from .models import Entry, Plant # entry is the sender
from django.dispatch import receiver # need to create a receiver
from django.utils import timezone

@receiver(post_save, sender=Entry) # every time  
def save_profile(sender, instance, **kwargs): 
    if instance.watered == "Y":
        instance.plant.last_watered = str(timezone.now())
        instance.plant.save(update_fields=['last_watered'])


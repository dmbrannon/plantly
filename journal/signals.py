from django.db.models.signals import post_save
from .models import Entry, Plant # entry is the sender
from django.dispatch import receiver # need to create a receiver
from django.utils import timezone

@receiver(post_save, sender=Entry) # every time  
def save_profile(sender, instance, **kwargs): 
    if instance.watered == "Y":
        instance.plant.last_watered = str(timezone.now())
        instance.plant.save(update_fields=['last_watered'])
    if instance.repotted == "Y":
        instance.plant.last_repotted = str(timezone.now())
        instance.plant.save(update_fields=['last_repotted'])
    if instance.fertilized == "Y":
        instance.plant.last_fertilized = str(timezone.now())
        instance.plant.save(update_fields=['last_fertilized'])
    if instance.treated == "Y":
        instance.plant.last_treated = str(timezone.now())
        instance.plant.save(update_fields=['last_treated'])


from django.contrib import admin
from .models import Plant, Entry

from image_cropping import ImageCroppingMixin

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(Entry)
admin.site.register(Plant, MyModelAdmin)

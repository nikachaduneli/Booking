from django.contrib import admin
from .models import Image, Place, ImageTn


admin.site.register(Place)
admin.site.register(Image)
admin.site.register(ImageTn)

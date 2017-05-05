from django.contrib import admin
from .models import Ingredient, Taste, AltName

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Taste)
admin.site.register(AltName)

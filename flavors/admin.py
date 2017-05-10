from django.contrib import admin
from .models import Ingredient, Taste, AltName

# Register your models here.
class AltNameInline(admin.TabularInline):
    model = AltName


class IngredientAdmin(admin.ModelAdmin):
    inlines = [
        AltNameInline,
    ]

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Taste)
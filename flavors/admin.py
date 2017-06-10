from django.contrib import admin
from .models import Ingredient, Taste, AltName, Combination, UserComboData

# Register your models here.
class AltNameInline(admin.TabularInline):
    model = AltName


class IngredientAdmin(admin.ModelAdmin):
    inlines = [
        AltNameInline,
    ]

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Taste)
admin.site.register(Combination)
admin.site.register(UserComboData)
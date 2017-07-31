from django.contrib import admin
from .models import Ingredient, AltName, Combination, UserComboData, IngredientSubmission

# Register your models here.
class AltNameInline(admin.TabularInline):
    model = AltName


class IngredientAdmin(admin.ModelAdmin):
    inlines = [
        AltNameInline,
    ]

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Combination)
admin.site.register(UserComboData)
admin.site.register(IngredientSubmission)
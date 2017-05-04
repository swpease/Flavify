from django.shortcuts import render, get_object_or_404

from .models import Ingredient, Taste


def index(request):
    pass


def pairings(request, ingredient):
    ingredient_spaced = ingredient.replace('-', ' ')
    ingredient_entry = get_object_or_404(Ingredient, base_item__exact=ingredient_spaced)
    context = {'ingredient': ingredient_entry}
    return render(request, 'flavors/ingredient.html', context)
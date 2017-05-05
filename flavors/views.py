from django.shortcuts import render, get_object_or_404

from .models import Ingredient, Taste, AltName


def index(request):
    pass


def pairings(request, ingredient):
    ingredient_spaced = ingredient.replace('-', ' ')
    alt_name = get_object_or_404(AltName, name__iexact=ingredient_spaced)
    context = {'altName': alt_name}
    return render(request, 'flavors/ingredient.html', context)

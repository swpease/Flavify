from django.shortcuts import render, get_object_or_404

from .models import Ingredient, Taste, AltName


def index(request):
    pass


def pairings(request, ingredient):
    """
    Context objects:
      :altName: AltName object. The requested ingredient.
      :listing: Ingredient object of the requested ingredient.
      :combos: list of QuerySets of Ingredients
    """
    ingredient_spaced = ingredient.replace('-', ' ')
    alt_name = get_object_or_404(AltName, name__iexact=ingredient_spaced)
    listing = alt_name.ingredient
    combos = listing.combination_set.all()
    complements = []
    for combo in combos:
        combo_filtered = combo.ingredients.exclude(listed_name__iexact=listing.listed_name)
        complements.append(combo_filtered)
    context = {'altName': alt_name, 'listing': listing, 'combos': complements}
    return render(request, 'flavors/ingredient.html', context)

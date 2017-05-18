from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Ingredient, Taste, AltName
from .forms import CombinationForm

def index(request):
    pass


def submit_combo(request):
    if request.method == 'POST':
        form = CombinationForm(request.POST)
        if form.is_valid():
            # TODO actually put the info in the db.
            return HttpResponseRedirect('/ingredient/hazelnut')

    else:
        form = CombinationForm  # Do not need to instantiate apparently?

    return render(request, 'flavors/submit-combo.html', {'form': form})

def submit_ingredient(request):
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

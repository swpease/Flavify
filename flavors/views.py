import json
import urllib

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings

from .models import Ingredient, Taste, AltName, Combination, IngredientSubmission
from .forms import CombinationForm, IngredientSubmissionForm


def recaptcha_validation(request):
    """
    source: https://simpleisbetterthancomplex.com/tutorial/2017/02/21/how-to-add-recaptcha-to-django-site.html
    :param request: Django request object.
    :return: dict(?). Result of recaptcha validation.
    """
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())

    return result

def index(request):
    pass


def submit_combo(request):
    if request.method == 'POST':
        form = CombinationForm(request.POST)
        if form.is_valid():
            result = recaptcha_validation(request)
            if result['success']:
                # If I had a ModelForm, I could just use form.save()
                new_combo = Combination()
                new_combo.save()
                for ing in form.cleaned_data['ingredients']:
                    new_combo.ingredients.add(ing)
                return HttpResponseRedirect('/ingredient/shrimp')

            else:
                return HttpResponseRedirect('/ingredient/hazelnut')
            # TODO... decide on redirects.

    else:
        form = CombinationForm()

    return render(request, 'flavors/submit-combo.html', {'form': form})

def submit_ingredient(request):
    # if request.method == 'POST':
    #     form = IngredientSubmissionForm(request.POST)
    #     if form.is_valid():
    #         result = recaptcha_validation(request)
    #         if result['success']:
    #             form.save()
    #             return HttpResponseRedirect('/ingredient/shrimp')
    #         else:
    #             return HttpResponseRedirect('/ingredient/hazelnut')
    #         # TODO... decide on redirects.
    #
    # else:
    #     form = IngredientSubmissionForm()

    # return render(request, 'flavors/submit-ingredient.html', {'form': form})

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

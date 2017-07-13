import requests

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Count

from .models import Ingredient, Taste, AltName, Combination, IngredientSubmission, UserComboData
from .forms import CombinationForm, IngredientSubmissionForm


def recaptcha_validation(request):
    """
    source: https://simpleisbetterthancomplex.com/tutorial/2017/02/21/how-to-add-recaptcha-to-django-site.html
    :param request: Django request object.
    :return: dict(?). Result of recaptcha validation.
    """
    recaptcha_response = request.POST.get('g-recaptcha-response')
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    return result

def index(request):
    return HttpResponse("This is the index page for now.")

def submit_combo(request):
    if request.method == 'POST':
        form = CombinationForm(request.POST)
        if form.is_valid():
            result = recaptcha_validation(request)
            if result['success']:
                # If I had a ModelForm, I could just use form.save()
                new_combo = Combination(submittor=request.user)
                new_combo.save()
                for ing in form.cleaned_data['ingredients']:
                    new_combo.ingredients.add(ing)
                # By default, the submittor is assumed to "like" the combination.
                new_usercombodata = UserComboData(combination=new_combo, user=request.user, like=True)
                new_usercombodata.save()
                return HttpResponseRedirect('/')

            else:
                return HttpResponseRedirect('/ingredient/hazelnut')
            # TODO... decide on redirects.

    else:
        form = CombinationForm()

    return render(request, 'flavors/submit-combo.html', {'form': form})

def submit_ingredient(request):
    if request.method == 'POST':
        form = IngredientSubmissionForm(request.POST)
        if form.is_valid():
            result = recaptcha_validation(request)
            if result['success']:
                form.save()
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/ingredient/hazelnut')
            # TODO... decide on redirects.

    else:
        form = IngredientSubmissionForm()

    return render(request, 'flavors/submit-ingredient.html', {'form': form})


# NOTE: I am uncertain if there is any performance difference between calling methods here vs in the template.
@ensure_csrf_cookie
def pairings(request, ingredient):
    """
    Context objects:
      :altName: AltName object. The requested ingredient.
      :listing: Ingredient object of the requested ingredient.
      :combos: (a) if User: tuple of (list of QuerySets of Ingredients, instance of Combo, instance of associated UserComboData)
               (b) no User: tuple of (list of QuerySets of Ingredients, instance of Combo)
    """
    ingredient_spaced = ingredient.replace('-', ' ')
    alt_name = get_object_or_404(AltName, name__iexact=ingredient_spaced)
    listing = alt_name.ingredient
    context = {'altName': alt_name, 'listing': listing}
    return render(request, 'flavors/ingredient.html', context)


@ensure_csrf_cookie
def table(request, ingredient):
    sort = request.GET.get('sort', 'ingredient')
    # sort = "num_ings" if sort_raw == "ingredient" else sort_raw
    order_raw = request.GET.get('order', 'asc')
    limit = int(request.GET.get('limit'))
    offset = int(request.GET.get('offset'))

    ingredient_spaced = ingredient.replace('-', ' ')
    alt_name = get_object_or_404(AltName, name__iexact=ingredient_spaced)
    listing = alt_name.ingredient
    combos = Combination.objects.annotate(num_ings=Count('ingredients')).filter(ingredients=listing)

    if sort == "ingredient":
        order = "" if order_raw == "asc" else "-"
        ordered_combos = combos.order_by(order + 'num_ings')
    else:
        order = False if order_raw == "asc" else True
        combos_ing_sorted = combos.order_by('num_ings')
        if sort == "ratings":
            ordered_combos = sorted(combos_ing_sorted, key=lambda c: c.get_num_tried(), reverse=order)
        elif sort == "pctliked":
            ordered_combos = sorted(combos_ing_sorted, key=lambda c: c.calc_percent_likes(), reverse=order)
        else:
            raise ValueError

    data = {
        # May need to change this if I incorporate filtering.
        'total': combos.count(),
        'rows': []
    }

    if request.user.is_authenticated:
        for combo in ordered_combos[offset:(offset + limit)]:
            ings_filtered = combo.ingredients.exclude(listed_name__iexact=listing.listed_name)
            ings_concat = ' '.join([str(i) for i in ings_filtered])
            try:
                user_combo_data = UserComboData.objects.get(combination=combo, user=request.user)
            except ObjectDoesNotExist:
                user_combo_data = UserComboData()
            data['rows'].append({
                'ingredient': {'ingredients': ings_concat,
                               'ucd': user_combo_data.id,  # https://github.com/wenzhixin/bootstrap-table/issues/586
                               'cid': combo.id},
                'ratings': combo.get_num_tried(),
                'pctliked': combo.calc_percent_likes(),
                'like': {'like': user_combo_data.like, 'dislike': user_combo_data.dislike},
                'star': user_combo_data.favorite,
                'notes': user_combo_data.note
            })

    else:
        for combo in ordered_combos[offset:(offset + limit)]:
            ings_filtered = combo.ingredients.exclude(listed_name__iexact=listing.listed_name)
            ings_concat = ' '.join([str(i) for i in ings_filtered])
            data['rows'].append({
                'ingredient': ings_concat,
                #  Note: I am calculating these values twice now...
                'ratings': combo.get_num_tried(),
                'pctliked': combo.calc_percent_likes()
            })
    return JsonResponse(data)


def search(request):
    pk = request.GET['name']
    return redirect('flavors:pairings', ingredient=AltName.objects.get(pk=pk))

import requests
from ast import literal_eval

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Count
from django.urls import reverse
from django.contrib import messages

from .models import Ingredient, AltName, Combination, IngredientSubmission, UserComboData
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
    return HttpResponseRedirect('/')

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
                messages.success(request, 'Thank you for your submission!')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

            return HttpResponseRedirect(reverse('flavors:submit-combo'))

    else:
        form = CombinationForm()

    return render(request, 'flavors/submit-combo.html', {'form': form})

def submit_ingredient(request):
    """
    Allows users to submit new ingredients to the db. I currently plan on just manually checking their submissions
    for validity via the admin site.
    :param request: Contains the form data submitted by the user for inclusion in the db.
    :DB Modification: Adds a new IngredientSubmission entry into the db. Includes ingredient and submittor.
    """
    if request.method == 'POST':
        form = IngredientSubmissionForm(request.POST)
        if form.is_valid():
            result = recaptcha_validation(request)
            if result['success']:
                new_ingredient = form.save()
                new_ingredient.submittor = request.user.username
                new_ingredient.save(update_fields=['submittor'])
                messages.success(request, 'Thank you for your submission!')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

            return HttpResponseRedirect(reverse('flavors:submit-ingredient'))

    else:
        form = IngredientSubmissionForm()

    return render(request, 'flavors/submit-ingredient.html', {'form': form})


def table(request):
    sort = request.GET.get('sort', 'ingredient')
    order_raw = request.GET.get('order', 'asc')
    limit = int(request.GET.get('limit'))
    offset = int(request.GET.get('offset'))
    filters = literal_eval(request.GET.get('filter', '{}'))  # Converts to dictionary
    altname_ids_raw = request.GET.get('altnameids')  # empty == ""
    altname_ids = altname_ids_raw.split(',')

    ingredients = []

    if altname_ids != [""]:
        for altname_id in altname_ids:
            ingredients.append(AltName.objects.get(id=altname_id).ingredient)
    combos = Combination.objects.annotate(num_ings=Count('ingredients'))
    for ing in ingredients:
        combos = combos.filter(ingredients=ing)

    if filters:
        if filters.get('like'):
            combos = combos.filter(usercombodata__user=request.user, usercombodata__like=True)
        if filters.get('star'):
            combos = combos.filter(usercombodata__user=request.user, usercombodata__favorite=True)
        if filters.get('notes'):
            combos = combos.filter(usercombodata__user=request.user, usercombodata__note__icontains=filters['notes'])

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
        'total': combos.count(),
        'rows': []
    }

    if request.user.is_authenticated:
        for combo in ordered_combos[offset:(offset + limit)]:
            ings_concat = ', '.join([str(i) for i in combo.ingredients.all()])
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
            ings_concat = ', '.join([str(i) for i in combo.ingredients.all()])
            data['rows'].append({
                'ingredient': ings_concat,
                #  Note: I am calculating these values twice now...
                'ratings': combo.get_num_tried(),
                'pctliked': combo.calc_percent_likes()
            })
    return JsonResponse(data)


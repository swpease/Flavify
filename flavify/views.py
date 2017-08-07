import json

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from flavors.models import UserComboData, Combination, AltName


def home(request):
    return render(request, "flavify/index.html", {})


def home_files(request, filename):
    return render(request, filename, {}, content_type='text/plain')

def about(request):
    return render(request, "flavify/about.html", {})


@login_required
def submissions(request):
    """
    The user's profile page. Currently just shows two tables:
      1. All combinations they have liked/disliked/favorited/noted
      2. All of their submitted combinations
    """
    # TODO... make AJAX responsive.
    submitted_combos = Combination.objects.filter(submittor=request.user)
    return render(request, "flavify/submissions.html", {"submitted_combos": submitted_combos})


def ajax_update_ucd(request):
    """
    Ajax update for UserComboData entries based on user clicking on buttons (like, dislike, save)
    in any relevant table (i.e. the ingredient's page table, or the profile first table)
    :return:
    """
    # Is there any point to including a check if user is authenticated?
    if request.method == "POST":
        data = request.body.decode('utf-8')
        received_json_data = json.loads(data)

        ucd_id = received_json_data['ucd_id']
        combo_id = received_json_data['combo_id']
        field_to_update = received_json_data['which_changed']
        note = received_json_data['note']

        if ucd_id != "null":
            ucd = UserComboData.objects.get(pk=ucd_id)
            if field_to_update == "note":
                ucd.note = note
            else:
                original_val = getattr(ucd, field_to_update)  # Should be a boolean
                setattr(ucd, field_to_update, not original_val)

                if not original_val:
                    if field_to_update == "like":
                        ucd.dislike = False
                    elif field_to_update == "dislike":
                        ucd.like = False

            if not (ucd.like or ucd.dislike or ucd.favorite) and ucd.note == "":
                deleted_entry = ucd.delete()
            else:
                ucd.save()
        else:
            combo = Combination.objects.get(pk=combo_id)
            ucd = UserComboData(user=request.user, combination=combo)
            if field_to_update == "note":
                ucd.note = note
            else:
                setattr(ucd, field_to_update, True)
            ucd.save()

        return JsonResponse({
            "like": ucd.like,
            "dislike": ucd.dislike,
            "favorite": ucd.favorite,
            "note": str(ucd.note),
            "ucd_id": str(ucd.pk),
        })


def ajax_select2(request):
    """
    Populates the search results for the index page's navbar select2 widget.
    """
    search = request.GET['q']
    results = []

    perfect_match = AltName.objects.filter(name__iexact=search)
    results.extend([{"id": ing.pk, "text": str(ing)} for ing in perfect_match])

    starting_match = AltName.objects.filter(name__istartswith=search)
    results.extend([{"id": ing.pk, "text": str(ing)} for ing in starting_match if {"id": ing.pk, "text": str(ing)} not in results])

    all_matches = AltName.objects.filter(name__icontains=search)
    results.extend([{"id": ing.pk, "text": str(ing)} for ing in all_matches if {"id": ing.pk, "text": str(ing)} not in results])
    return JsonResponse({
        "results": results[:25]
    })

import json

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from flavors.models import UserComboData, Combination


def home(request):
    return render(request, "flavify/index.html", {})


def home_files(request, filename):
    return render(request, filename, {}, content_type='text/plain')


@login_required
def profile(request):
    """
    The user's profile page. Currently just shows two tables:
      1. All combinations they have liked/disliked/favorited/noted
      2. All of their submitted combinations
    """
    # TODO... make AJAX responsive.
    user_combo_data = UserComboData.objects.filter(user=request.user)
    submitted_combos = Combination.objects.filter(submittor=request.user)
    return render(request, "flavify/profile.html", {"user_combo_data": user_combo_data,
                                                "submitted_combos": submitted_combos})


def ajax_update_ucd(request):
    """
    Ajax update for UserComboData entries based on user clicking on buttons (like, dislike, save)
    in any relevant table (i.e. the ingredient's page table, or the profile first table)
    :return:
    """
    if request.method == "POST":
        data = request.body.decode('utf-8')
        received_json_data = json.loads(data)

        ucd_id = received_json_data['ucd_id']
        field_to_update = received_json_data['which_changed']
        if ucd_id is not None:
            ucd = UserComboData.objects.get(pk=ucd_id)
            original_val = getattr(ucd, field_to_update)  # Should be a boolean
            setattr(ucd, field_to_update, not original_val)

            if not (ucd.like or ucd.dislike or ucd.favorite) and ucd.note == "":
                deleted_entry = ucd.delete()
                # Do I want to return here?
            else:
                ucd.save()

        # else:
            # ucd = UserComboData(like=ucd_id["like"], dislike=ucd_id["dislike"], favorite=ucd_id["save"])
        return JsonResponse({'x': ucd_id})
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

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
import requests

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

from flavors.models import UserComboData, Combination


def home(request):
    return render(request, "flavify/index.html", {})


def home_files(request, filename):
    return render(request, filename, {}, content_type='text/plain')


def profile(request):

    user_combo_data = UserComboData.objects.filter(user=request.user)
    return render(request, "flavify/profile.html", {"user_combo_data": user_combo_data})

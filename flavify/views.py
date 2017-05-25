import requests

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings


def home(request):
    return render(request, "flavify/index.html", {})

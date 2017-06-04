"""flavify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

# ref: https://stackoverflow.com/questions/7013735/turn-off-caching-of-static-files-in-django-development-server
from django.conf import settings
from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$', views.home_files, name='home_files'),
    url(r'^ingredient/', include('flavors.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns.append(url(r'^static/(?P<path>.*)$', never_cache(serve_static)))

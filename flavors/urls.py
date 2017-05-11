from django.conf.urls import url

from . import views


app_name = 'flavors'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<ingredient>.+)/$', views.pairings, name='pairings'),
]
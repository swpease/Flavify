from django.conf.urls import url

from . import views


app_name = 'flavors'
urlpatterns = [
    url(r'^$', views.index, name='index'), # TODO... do I want this?
    url(r'^submit-combo/', views.submit_combo, name='submit-combo'),
    url(r'^submit-ingredient/', views.submit_ingredient, name='submit-ingredient'),
    url(r'^(?P<ingredient>.+)/$', views.pairings, name='pairings'),
]
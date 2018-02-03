from django.conf.urls import url
# from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^dashboard$', views.dashboard),
    url(r'^add_plan$', views.add_plan),
    url(r'^destination', views.destination)

]
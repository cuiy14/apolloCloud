"""define the url mode of forecast app""" 

from django.conf.urls import url

from . import views

urlpatterns=[
    #main page for each user, containing the upload records
    url(r'^$', views.records, name='records'),
    #upload page
    url(r'^upload/$', views.upload, name='upload'),
]

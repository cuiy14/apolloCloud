"""define the urls mode of urls app"""

from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns=[
    #login page, the views.function use the provided one
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
    #index page
    url(r'^$', views.index, name='index'),
    #register page
    url(r'^register/$', views.register, name='register'),
    #log out page
    url(r'^logout/$', views.logout_view, name='logout'),
]

"""define the url mode of forecast app""" 

from django.conf.urls import url

from . import views

urlpatterns=[
    #main page for each user, containing the upload records
    url(r'^$', views.records, name='records'),
    #upload page
    url(r'^upload/$', views.upload, name='upload'),
    #detailed description for a single upload item
    url(r'^item/(?P<upload_id>\d+)/$', views.item, name='item'),
    #the link for download the primary data file
    url(r'^itemdownload/(?P<upload_id>\d+)/$', views.itemdownload, name='itemdownload'),
    # the link for downloading the result file
    url(r'^resultFile/(?P<fileUrl>.+)/$', views.resultFile, name='resultFile'),
]

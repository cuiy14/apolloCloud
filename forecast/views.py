# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from forecast.models import Upload
from forecast.forms import UploadForm

# Create your views here.

@login_required
def records(request):
    """show all records of a specific user"""
    records = Upload.objects.filter(owner=request.user).order_by('-date_added')
    context = {'records':records}
    return render(request, 'forecast/index.html', context)


@login_required
def upload(request):
    """the page for upload files containing the data"""
    if request.method != 'POST':
        uploadForm = UploadForm()
    else:
        uploadForm = UploadForm(request.POST, request.FILES)
        if uploadForm.is_valid():
            new_uploadForm = uploadForm.save(commit=False)
            new_uploadForm.owner = request.user
            new_uploadForm.save()
            return HttpResponseRedirect(reverse('users:index'))
            #the page to redirect should be modified, i.e., the records or result page
    context = {'uploadForm':uploadForm}
    return render(request, 'forecast/upload.html', context)

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse,Http404, StreamingHttpResponse
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
            return HttpResponseRedirect(reverse('forecast:records'))
            #the page to redirect should be modified, i.e., the records or result page
    context = {'uploadForm':uploadForm}
    return render(request, 'forecast/upload.html', context)

@login_required
def item(request, upload_id):
    """the detailed description for a upload item"""
    upload = Upload.objects.get(id=upload_id)
    if upload.owner != request.user:
        raise Http404

    context = {'upload':upload}
    return render(request, 'forecast/item.html',context)

@login_required #this is not necessary
def itemdownload(request,upload_id):
    def file_iterator(file_name,chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    upload = Upload.objects.get(id=upload_id)
    filename='upload' + os.sep + str(upload.userfiles)  #this may needed changing if the location of files downloading is varing
    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content--Disposition'] = 'attachment;filename="{0}"'.format(filename)

    return response


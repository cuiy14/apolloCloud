# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename):
    #file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

def user_file_name(instance, filename):
    return '{0}'.format(filename)

class Upload(models.Model):
    """the upload record item for each forecast"""
    owner = models.ForeignKey(User)
    FORECASTPERIOD = (
        ('s', 'short term'),
        ('m', 'medium term'),
        ('l', 'long term'),
        )
    FORECASTMETHOD =(
        ('ann', 'neural network'),
        ('svm', 'support vector machine'),
        ('mps', 'multiple proportion smoothing method')
        )
    #the max_length limits the length of key
    #blank & default is to remove the '---' in the model form; the fist parameter is for the label of the form
    forecastperiod = models.CharField("Forecasting period", max_length=1, choices=FORECASTPERIOD, blank=False, default='m')            
    forecastmethod = models.CharField("Forecasting method", max_length=3, choices=FORECASTMETHOD, blank=False, default='ann')         
    userfiles = models.FileField(upload_to = user_directory_path)
    #uploadname=models.CharField(user_file_name())
    date_added = models.DateTimeField(auto_now_add =True)
    

    def __unicode__(self):
        """return the string format of the upload record"""
        return str(self.date_added)

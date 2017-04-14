# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename):
    #file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

class Upload(models.Model):
    """the upload record item for each forecast"""
    owner = models.ForeignKey(User)
    userfiles = models.FileField(upload_to = user_directory_path)
    date_added = models.DateTimeField(auto_now_add =True)

    def __unicode__(self):
        """return the string format of the upload record"""
        return self.date_added

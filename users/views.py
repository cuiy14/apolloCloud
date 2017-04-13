# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    """the main page of apolloCloud platform"""
    return render(request, 'users/index.html')

def logout_view(request):
    """log out and redirect to the index page"""
    logout(request)
    return HttpResponseRedirect(reverse('users:index'))

def register(request):
    """register"""
    if request.method != 'POST':
        #show the empty register form
        form = UserCreationForm()
    else:
        #process the register form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #let the user login automatically, and redirect to the main page
            authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('users:index'))

    context = {'form':form}
    return render(request,'users/register.html', context)

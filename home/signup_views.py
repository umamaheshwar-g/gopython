# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from quiz.forms import UserForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout




# Create your views here.
def index(request):
	return HttpResponseRedirect('/login/')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid() :
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors,)
    else:
        user_form = UserForm()
    return render(request,'signup_templates/registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                next_url=request.POST.get('next', None)
                print(request.GET)
                print('next_url',next_url)
                if next_url:
                    print('next_url',next_url)
                    return HttpResponseRedirect(next_url)
                else:
                    # return HttpResponseRedirect(reverse('quiz:start'))
                    return HttpResponseRedirect(reverse('quiz:generate'))
                    # return redirect('/user_login/')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'signup_templates/login.html', {})


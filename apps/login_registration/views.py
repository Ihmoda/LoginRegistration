# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.contrib import messages

from .models import User

import bcrypt


# Create your views here.
def index(request):
    return render(request, "login_registration/index.html")

def register(request):
    print "hit registration"
    
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            unhashed = request.POST['password']
            hash1 = bcrypt.hashpw(unhashed.encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash1, birthday=request.POST['birthday'])
            messages.success(request, "Registered successfully")
            request.session['userid'] = new_user.id
            return redirect('/success')
        
    return redirect('/')


def success(request):

    if 'userid' in request.session:
        context = {
            "first_name": User.objects.get(id=request.session['userid']).first_name
        }

        print User.objects.get(id=request.session['userid']).first_name
        return render(request, "login_registration/success.html", context)
    else:
        return redirect('/')


def login(request):
    
    if request.method == "POST":
        unhashedpw = request.POST['password']
        email = request.POST['email']

        login_user = User.objects.filter(email=email)
        if len(login_user) == 0:
            messages.error(request, "Incorrect username or password")
            return redirect('/')
        else:
            hashedpw = login_user[0].password
            if bcrypt.checkpw(unhashedpw.encode(), hashedpw.encode()):
                request.session['userid'] = login_user[0].id
                return redirect('/success')

    return redirect('/')

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
import os
import sys
import subprocess
import json
import sqlite3
import hashlib
from sqlite3 import OperationalError
from . import models

def hash_code(source):
    hash = hashlib.sha256()
    hash.update(source.encode())
    return hash.hexdigest()

def event(request, action):
    context = {
        "registered": [],
        "all": [],
        "detail": None
    }
    current_user = models.User.objects.get(email=request.session["email"])
    registered_event = models.User_Event.objects.get(user=current_user)
    if action == "detail":
        event = models.Event.objects.get(eid=request.GET["eid"])
        context["detail"] = event
        return render(request, 'detail.html', context)
    elif action == "register":
        event = models.Event.objects.get(eid=request.GET["eid"])
        new_registration = models.User_Event(user=current_user, event=event)
        new_registration.save()
    elif action == "add":
        new_event = models.Event(eid=(models.Event.objects.all().last().eid + 1), title=request.POST["title"], description=request.POST["description"], picture=request.POST["picture"])
        new_event.save()
    else:
        pass
    context["all"] = models.Event.objects.all()
    context["registered"] = models.User_Event.objects.get(user=current_user)
    return render(request, 'event.html', context)

def user(request, action):
    context = {}
    if action == "register":
        new_user = models.User(email=request.POST["email"], password=hash_code(request.POST["password"])
        new_user.save()
    elif action == "login":
        user = models.User.objects.get(email=request.POST["email"])
        if user.password == hash_code(request.POST["password"]):
            request.session["email"] = user.email
            request.session["password"] = user.password
            request.session["user_login"] = True
    elif action == "logout":
        request.session.flush()
    return redirect("/")

def manage(request):
    pass

def about(request):
    context = {}
    context["events"] = models.About.objects.all()
    return render(request, 'about.html', context)

def index(request):
    context = {}
    if "user_login" in request.session and request.session["user_login"]:
        context["user_login"] = request.session["email"]
    return render(request, 'index.html', context)

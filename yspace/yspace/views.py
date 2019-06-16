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
        "all": []
    }
    new_event = models.Event()
    new_event.eid = 0
    new_event.title = "Event Title"
    new_event.description = "Event Description"
    new_event.picture = "Event_Picture"
    context["registered"].append(new_event)
    if action == "detail":
        return render(request, 'detail.html', context)
    else:
        return render(request, 'event.html', context)

def user(request, action):
    context = {}
    if action == "register":
        new_user = models.User()
        new_user.email = request.POST["email"]
        new_user.password = hash_code(request.POST["password"])
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
    context["events"] = [
        ["Point", "Time", "Title", "This is context."]
    ]
    return render(request, 'about.html', context)

def index(request):
    context = {}
    if "user_login" in request.session and request.session["user_login"]:
        context["user_login"] = request.session["email"]
    return render(request, 'index.html', context)

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
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
    temp_resgitered = {
        "ID": 0,
        "Title": "Event Title",
        "Description": "Event Description",
        "Picture": "Event_Picture"
    }
    context["registered"].append(temp_resgitered)
    if action == "detail":
        return render(request, 'detail.html', context)
    else:
        return render(request, 'index.html', context)

def user(request, action):
    context = {}
    if action == "register":
        new_user = models.User()
        new_user.email = request.POST["email"]
        new_user.password = hash_code(request.POST["password"])
        new_user.save()
    elif action == "login":
        pass
    elif action == "logout":
        pass
    return render(request, 'index.html', context)

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
    return render(request, 'index.html', context)

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import os
import sys
import subprocess
import json
import sqlite3
from sqlite3 import OperationalError

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
    if action == "register":
        pass
    elif action == "login":
        pass
    elif action == "logout":
        pass
    else:
        pass

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

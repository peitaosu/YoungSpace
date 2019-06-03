from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import os
import sys
import subprocess
import json
import sqlite3
from sqlite3 import OperationalError

def event(request):
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
    return render(request, 'event.html', context)

def join(request):
    pass

def user(request):
    pass

def register(request):
    pass

def login(request):
    pass

def logout(request):
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

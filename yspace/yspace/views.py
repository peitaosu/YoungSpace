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
    pass

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
    pass

def index(request):
    context = {}
    return render(request, 'index.html', context)

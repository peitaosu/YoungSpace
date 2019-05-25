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

def user(request):
    pass

def manage(request):
    pass

def index(request):
    context = {}
    return render(request, 'index.html', context)

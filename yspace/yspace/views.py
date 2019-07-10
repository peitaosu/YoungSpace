from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
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

def if_not_login(request):
    if "email" not in request.session:
        return True
    return False

def if_not_staff(request):
    current_user = models.User.objects.get(email=request.session["email"])
    if not current_user.is_staff:
        return True
    return False

def show_login_user(request, context):
    if "email" in request.session:
        current_user = models.User.objects.get(email=request.session["email"])
        if current_user.name != "":
            context["user_login"] = current_user.name
        else:
            context["user_login"] = request.session["email"]
    return context

def event(request, action):
    if settings.MAINTENANCE_MODE:
        return redirect("/")
    context = {
        "registered": [],
        "all": [],
        "detail": None
    }
    if if_not_login(request):
        return redirect("/")
    context = show_login_user(request, context)
    current_user = models.User.objects.get(email=request.session["email"])
    if action == "/detail":
        event = models.Event.objects.get(eid=request.GET["eid"])
        context["detail"] = event
        return render(request, 'detail.html', context)
    elif action == "/register":
        event = models.Event.objects.get(eid=request.GET["eid"])
        new_registration = models.User_Event(user=current_user, event=event)
        new_registration.save()
        return redirect("/event/my")
    elif action == "/cancel":
        event = models.Event.objects.get(eid=request.GET["eid"])
        user_event = models.User_Event.objects.get(user=current_user, event=event)
        user_event.delete()
        return redirect("/event/my")
    elif action == "/add":
        if if_not_staff(request):
            return redirect("/")
        new_event = models.Event(eid=(models.Event.objects.all().last().eid + 1), title=request.POST["title"], description=request.POST["description"], picture=request.POST["picture"])
        new_event.save()
        return redirect("/event/all")
    else:
        context["all"] = models.Event.objects.all()
        registered_events = models.User_Event.objects.all().filter(user=current_user)
        for user_event in registered_events:
            context["registered"].append(user_event.event)
        if action == "/my":
            return render(request, 'event_my.html', context)
        elif action == "/all":
            return render(request, 'event_all.html', context)
        else:
            return redirect("/event/all")

def user(request, action):
    if settings.MAINTENANCE_MODE:
        return redirect("/")
    if action == "/register":
        if models.User.objects.filter(email=request.POST["email"]).count() > 0:
            context = {
                "has_alert": True,
                "alertclass": "alert-danger",
                "alertmessage": "You email address was already registered, please check again."
            }
            messages.info(request, "You email address was already registered, please check again.")
            return render(request, 'index.html', context)
        new_user = models.User(email=request.POST["email"], password=hash_code(request.POST["password"]))
        new_user.save()
        request.session["email"] = new_user.email
        request.session["user_login"] = True
        return redirect("/user")
    elif action == "/update":  
        if if_not_login(request):
            return redirect("/")
        user = models.User.objects.get(email=request.session["email"])
        user.name = request.POST["name"]
        if "gender" in request.POST and request.POST["gender"] != "N":
            user.gender = request.POST["gender"]
        if "age" in request.POST and request.POST["age"] != "":
            user.age = request.POST["age"]
        user.career = request.POST["career"]
        user.biography = request.POST["biography"]
        if "picture" in request.FILES:
            file_upload = request.FILES['picture']
            fs = FileSystemStorage()
            file_name = fs.save(file_upload.name, file_upload)
            file_url = fs.url(file_name)
            user.picture = file_url
        user.save()
    elif action == "/login":
        if models.User.objects.filter(email=request.POST["email"]).count() == 0:
            context = {
                "has_alert": True,
                "alertclass": "alert-danger",
                "alertmessage": "You email was not registered, please check again or register this email."
            }
            return render(request, 'index.html', context)
        user = models.User.objects.get(email=request.POST["email"])
        if user.password == hash_code(request.POST["password"]):
            request.session["email"] = user.email
            request.session["user_login"] = True
    elif action == "/logout":
        request.session.flush()
    else:
        context = show_login_user(request, {})
        context["profile"] = models.User.objects.get(email=request.session["email"])
        return render(request, 'profile.html', context)
    return redirect("/")

def manage(request):
    if settings.MAINTENANCE_MODE:
        return redirect("/")
    context = {}
    if if_not_login(request):
        return redirect("/")
    context = show_login_user(request, context)
    current_user = models.User.objects.get(email=request.session["email"])
    if if_not_staff(request):
        context = {
                "has_alert": True,
                "alertclass": "alert-danger",
                "alertmessage": "You are not staff, you can not access this page."
            }
        return render(request, 'index.html', context)
    return render(request, 'manage.html', context)

def about(request):
    if settings.MAINTENANCE_MODE:
        return redirect("/")
    context = {}
    context = show_login_user(request, context)
    context["events"] = models.About.objects.all()
    return render(request, 'about.html', context)

def index(request):
    context = {}
    context["MAINTENANCE_MODE"] = settings.MAINTENANCE_MODE
    context = show_login_user(request, context)
    return render(request, 'index.html', context)

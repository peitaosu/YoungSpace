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

def redirect_if_not_login(request):
    if "email" not in request.session:
        return redirect("/")

def redirect_if_not_staff(request):
    current_user = models.User.objects.get(email=request.session["email"])
    if not current_user.is_staff:
        return redirect("/")

def show_login_user(request, context):
    if "email" in request.session:
        context["user_login"] = request.session["email"]
    return context

def event(request, action):
    context = {
        "registered": [],
        "all": [],
        "detail": None
    }
    redirect_if_not_login(request)
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
        redirect_if_not_staff(request)
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
    context = {}
    redirect_if_not_login(request)
    context = show_login_user(request, context)
    if action == "/register":
        new_user = models.User(email=request.POST["email"], password=hash_code(request.POST["password"]))
        new_user.save()
        request.session["email"] = new_user.email
        request.session["user_login"] = True
        return redirect("/user")
    elif action == "/login":
        user = models.User.objects.get(email=request.POST["email"])
        if user.password == hash_code(request.POST["password"]):
            request.session["email"] = user.email
            request.session["user_login"] = True
    elif action == "/logout":
        request.session.flush()
    else:
        context["profile"] = models.User.objects.get(email=request.session["email"])
        return render(request, 'profile.html', context)
    return redirect("/")

def manage(request):
    context = {}
    redirect_if_not_login(request)
    context = show_login_user(request, context)
    current_user = models.User.objects.get(email=request.session["email"])
    redirect_if_not_staff(request)
    return render(request, 'manage.html', context)

def about(request):
    context = {}
    context["events"] = models.About.objects.all()
    return render(request, 'about.html', context)

def index(request):
    context = {}
    context = show_login_user(request, context)
    return render(request, 'index.html', context)

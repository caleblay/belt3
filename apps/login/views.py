# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User, Plan
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

def index(request):
    request.session.flush()
    return render(request, 'login/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/success')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    request.session['full_name'] = result.first_name +" "+result.last_name
    messages.success(request, "Successfully logged in!")
    return redirect('/dashboard')

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'login/success.html', context)

def dashboard(request):
    if not request.session.get("user_id"):
        return redirect ('/')
    plans = Plan.objects.get(planned_by=request.session['user_id'])
    if isinstance(plans,Plan):
        plans = [plans] 
    else:
        plans=list(Plan.objects.get(planned_by=request.session['user_id']))
    other_plans = Plan.objects.all().exclude(planned_by=request.session['user_id'])
    context = {
        'data': plans,
        'user': User.objects.get(id=request.session['user_id']),
        'other_plans': other_plans
    }
    return render(request, 'login/dashboard.html', context)

def add_plan(request):
    if not request.session.get("user_id"):
        return redirect ('/')
    if (request.POST):
        current_user = User.objects.get(id=request.session['user_id'])
        planned_by = str(current_user.id)
        destination = request.POST.get('destination')
        description = request.POST.get('description')
        traveled_to = datetime.strptime(request.POST.get('traveled_to'), '%m-%d-%Y')
        traveled_from = datetime.strptime(request.POST.get('traveled_from'), '%m-%d-%Y')
        newplan = Plan(destination=destination, planned_by=planned_by, description=description, traveled_to=traveled_to, traveled_from=traveled_from)
        newplan.save()
        return redirect('/dashboard')
    else:
        return render(request, 'login/add_plan.html')


def destination(request):
    id_plan = request.GET.get('id')
    plans = Plan.objects.get(id=int(id_plan))
    context = {
        'plans': plans
    }
    return render (request, 'login/destination.html', context)


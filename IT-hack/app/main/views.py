from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from threading import Thread
from datetime import date
from .models import *
import os

email_server = settings.EMAIL_HOST_USER


def is_email(data):
    try:
        validate_email(data)
    except:
        return False
    else:
        return True
    

def SMS_email(subject, text, emails):
    send_mail(subject, text, email_server, emails, fail_silently=False)


def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        _login = request.POST['login']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(_login, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user = authenticate(request, username=_login, password=password)

            login(request, user)

            thread = Thread(target=send_mail,args=("Регистрация", f"Здравствуйте, {last_name} {first_name}, Вы успешно зарегистрировались на PlaceKvant!", email_server, [email]))
            thread.start()
            return redirect('/login')
        except Exception as ex:
            print(ex)
            return redirect('/register')
    else:
        return render(request, 'register.html')
    

def logout_page(request):
    logout(request)
    return redirect('/login')


def login_page(request):
    if request.method == 'POST':
        _login = request.POST['login']
        password = request.POST['password']
        if is_email(_login):
            user = User.objects.filter(email=_login).first()
            _login = user.username
            user = authenticate(request, username=_login, password=password)
            if user is not None:
                login(request, user)
                return redirect('/profile')
            else:
                return redirect('/login')
        else:
            user = authenticate(request, username=_login, password=password)
            if user is not None:
                login(request, user)
                return redirect('/profile')
            else:
                return redirect('/login')
    else:
        return render(request, 'login.html')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    return render(request, 'profile.html')


def profile_edit(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    user = User.objects.filter(username=_login).first()
    if request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        if old_password != '' and new_password != '':
            if not user.check_password(old_password):
                return redirect('/profile_edit')
            if (old_password == '' and new_password != '') or (old_password != '' and new_password == ''):
                return redirect('/profile_edit')
            user.set_password(new_password)
        user.save()
        login(request, user)
        return redirect('/profile')
    else:
        context = {
            'user': user
        }
        return render(request, 'profile_edit.html', context=context)
    

def add_place(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    user = User.objects.filter(username=_login).first()
    if not user.is_staff:
        return redirect('/login')
    if request.POST:
        try:
            name = request.POST['name']
            description = request.POST['description']
            places = int(request.POST['places'])
            image = request.FILES['image']

            place_obj = Place(author=_login, name=name,description=description, image=image, places=places)
            place_obj.save()
            return redirect('/')
        except Exception as ex:
            print(ex)
            return redirect('/add_place')
    else:
        return render(request, 'add_place.html')
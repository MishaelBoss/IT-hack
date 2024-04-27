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
    query = str(request.GET.get('query', ''))
    if query is None:
        all_places = list(Place.objects.all().order_by('-id').all())
    else:
        all_places = []
        for i in list(Place.objects.all().order_by('-id')):
            if query.lower() in i.name.lower() or i.name.lower() in query.lower():
                all_places.append(i)
    places = []
    for i in all_places:
        places.append(i)
    i_participate = []
    delta_s = []
    delta_ss = []
    for place in places:
        if PlaceMember.objects.filter(user=_login, place_id=place.id).first() is None:
            i_participate.append(False)
        else:
            i_participate.append(True)

        delta_s.append((place.to_date-date.today()).days)
        delta_ss.append((place.from_date-date.today()).days)

    if query is None or query == 'None':
        query = ''
    context = {
        'places': list(zip(places, i_participate, delta_s, delta_ss)),
        'query': query
    }
    return render(request, 'index.html', context=context)


def admin_panel(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    query = str(request.GET.get('query', ''))
    if query is None:
        all_places = list(Place.objects.all().order_by('-id').all())
    else:
        all_places = []
        for i in list(Place.objects.all().order_by('-id')):
            if query.lower() in i.name.lower() or i.name.lower() in query.lower():
                all_places.append(i)
    places = []
    for i in all_places:
        places.append(i)
    i_participate = []
    delta_s = []
    delta_ss = []
    for place in places:
        if PlaceMember.objects.filter(user=_login, place_id=place.id).first() is None:
            i_participate.append(False)
        else:
            i_participate.append(True)

        delta_s.append((place.to_date-date.today()).days)
        delta_ss.append((place.from_date-date.today()).days)

    if query is None or query == 'None':
        query = ''

    context = {
        'places': list(zip(places, i_participate, delta_s, delta_ss)),
        'query': query
    }
    return render(request, 'admin_panel.html', context=context)


def place_members(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    if not request.user.is_staff:
        return redirect('/login')
    pr_id = int(request.GET['id'])
    tbs = Place_roomMember.objects.filter(pr_id=pr_id).all()
    context = {
        'tbs': tbs,
        'pr_id': pr_id
    }
    return render(request, 'place_members.html', context=context)


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

            thread = Thread(target=send_mail, args=("Регистрация",
                            f"Здравствуйте, {last_name} {first_name}, Вы успешно зарегистрировались на PlaceKvant! Через год меняйте пароль!", email_server, [email]))
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
    pl = Place_roomMember.objects.filter(user=_login).first()
    place_obj = Place.objects.filter().first()
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
            number_of_seats = int(request.POST['number_of_seats'])
            is_solo = request.POST['is_solo'] == 'public'
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            image = request.FILES['image']

            place_obj = Place(author=_login, name=name, description=description, 
                              number_of_seats=number_of_seats, from_date=from_date, to_date=to_date, image=image, is_solo=is_solo)
            place_obj.save()
            return redirect('/')
        except Exception as ex:
            print(ex)
            return redirect('/add_place')
    else:
        return render(request, 'add_place.html')


def delete_place(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    place_id = int(request.GET['place_id'])

    place = Place.objects.filter(id=place_id).first()
    if place.author != _login:
        return redirect('/login')
    emails = [User.objects.filter(username=i.user).first().email for i in PlaceMember.objects.filter(place_id=place_id)]
    for i in PlaceMember.objects.filter(place_id=place_id).all():
        i.delete()
    place.delete()
    
    thread = Thread(target=SMS_email,
                                 args=("Изменения", f"Здравствуйте, событие {place.name} удалили!", emails))
    thread.start()
    return redirect('/admin_panel')


def edit_place(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    place_id = int(request.GET['place_id'])

    place = Place.objects.filter(id=place_id).first()
    if place.author != _login:
        return redirect('/login')
    
    if request.POST:
        try:
            place.name = request.POST['name']
            place.description = request.POST['description']
            place.number_of_seats = int(request.POST['number_of_seats'])
            place.is_solo = request.POST['is_solo'] == 'public'
            place.from_date = request.POST['from_date']
            place.to_date = request.POST['to_date']
        
            if request.FILES.get('image') is not None:
                place.image = request.FILES['image']
            emails = [User.objects.filter(username=i.user).first().email for i in PlaceMember.objects.filter(place_id=place_id)]
            thread = Thread(target=SMS_email,
                                         args=("Изменения", f"Здравствуйте, на событии {place.name} произошли изменения. Обратите, пожалуйста, внимание!", emails))
            thread.start()
            place.save()
        except Exception as ex:
            print(ex)
            return redirect(f'/edit_place?place_id={place_id}')
        return redirect('/admin_panel')
    else:
        context = {
            'place':place
        }
        return render(request, 'edit_place.html', context=context)


def place_more(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    place_id = int(request.GET['id'])

    place_rooms = Place_room.objects.filter().all().order_by('-id')
    place = Place.objects.filter(id=place_id).first()
    email = User.objects.filter(username=place.author).first().email

    context = {
        'place_rooms': place_rooms,
        'place': place,
        'email': email
    }
    return render(request, 'place_more.html', context=context)


def add_place_room(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    user = User.objects.filter(username=_login).first()
    if not user.is_staff:
        return redirect('/login')
    if request.POST:
        try:
            place_room_int = request.POST['place_room_int']

            place_room_obj = Place_room(place_room_int=place_room_int)
            place_room_obj.save()
            return redirect('/')
        except Exception as ex:
            print(ex)
            return redirect('/add_place_room')
    else:
        return render(request, 'add_place_room.html')
    

def edit_place_room(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    place_room_id = int(request.GET['place_room_id'])

    place_room = Place_room.objects.filter(id=place_room_id).first()
    if request.POST:
        try:
            place_room.place_room_int = request.POST['place_room_int']
        
            place_room.save()
        except Exception as ex:
            print(ex)
            return redirect(f'/edit_place_room?place_room_id={place_room_id}')
        return redirect('/admin_panel')
    else:
        context = {
            'place_room':place_room
        }
        return render(request, 'edit_place_room.html', context=context)
    

def delete_place_room(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    place_room_id = int(request.GET['place_room_id'])

    place_room = Place_room.objects.filter(id=place_room_id).first()
    place_room.delete()
    return redirect('/')


def buy(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    pr_id = int(request.GET['id'])
    place_obj = Place.objects.filter(id=pr_id).first()
    if request.POST:
        try:
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']

            if place_obj.number_of_seats > 0:
                pl = Place_roomMember(user=_login, pr_id=pr_id, 
                                      from_date=from_date, to_date=to_date)
                pl.save()
                place_obj.number_of_seats -= 1
                place_obj.save()
            return redirect(f'/place_more?id={pr_id}')
        except Exception as ex:
            print(ex)
            return redirect(f'/buy?id={pr_id}')
    else:
        context = {
            'place_obj': place_obj
        }
        return render(request, 'buy.html', context=context)
    

def buygroup(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    _login = request.user.username
    pr_id = int(request.GET['id'])
    place_obj = Place.objects.filter(id=pr_id).first()
    if request.POST:
        try:
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']

            usernames = []
            post_data = dict(request.POST.lists())
            keys = list(post_data.keys())
            for key in keys:
                if key[0:4] == 'user':
                    usernames.append(post_data[key][0])
            if place_obj.number_of_seats - len(usernames) > 0:
                for username in usernames:
                    user = User.objects.filter(username=username).first()
                    if user is not None:
                        pl = Place_roomMember(user=username, pr_id=pr_id, 
                                      from_date=from_date, to_date=to_date)
                        pl.save()
                place_obj.number_of_seats -= len(usernames)
                place_obj.save()
            return redirect(f'/place_more?id={pr_id}')
        except Exception as ex:
            print(ex)
            return redirect(f'/buygroup?id={pr_id}')
    else:
        context = {
            'place_obj': place_obj
        }
        return render(request, 'buygroup.html')
    

# def buy_remove(request):
#     if not request.user.is_authenticated:
#         return redirect('/login')
#     _login = request.user.username
#     pr_id = int(request.GET['id'])
#     pr = Place_roomMember.objects.filter(id=pr_id).first()
#     place_obj = Place.objects.filter(id=pr.pr_id).first()
#     try:
#         pr.delete()
#         place_obj.number_of_seats += 1
#         place_obj.save()
#         return redirect('/')
#     except:
#         return redirect('/')


def send_faq(request):
    if not request.user.is_authenticated:
       return redirect('/login')
    _login = request.user.username
    user = User.objects.filter(username=_login).first()

    if request.POST:
        author = user.username
        email = user.email
        message = request.POST['message']
        faq = FAQMessage(author=author, email=email, message=message)
        faq.save()
        return redirect('/')
    else:
        return render(request, 'send_faq.html')
    

def read_faq_messages(request):
    if not request.user.is_authenticated:
       return redirect('/login')
    _login = request.user.username
    user = User.objects.filter(username=_login).first()
    if not user.is_staff:
        return redirect('/login')
    
    faqs = FAQMessage.objects.all().order_by('-id')

    context = {
        'faqs': faqs
    }

    return render(request, 'read_faqs.html', context=context)


def view_faq(request):
    if not request.user.is_authenticated:
       return redirect('/login')
    _login = request.user.username
    user = User.objects.filter(username=_login).first()
    if not user.is_staff:
        return redirect('/login')
    faq_id = int(request.GET['faq_id'])
    faq = FAQMessage.objects.filter(id=faq_id).first()
    context = {
        'faq': faq
    }
    return render(request, 'view_faq.html', context=context)


def delete_faq(request):
    if not request.user.is_authenticated:
       return redirect('/login')
    _login = request.user.username
    user = User.objects.filter(username=_login).first()
    if not user.is_staff:
        return redirect('/login')
    faq_id = int(request.GET['faq_id'])
    faq = FAQMessage.objects.filter(id=faq_id).first()
    faq.delete()
    return redirect('/read_faqs')
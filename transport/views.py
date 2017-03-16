from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .models import SiteUser, User
# Create your views here.


def index(request):
    message = request.GET.get('message')
    if message is not None:
        box = True
    else:
        box = False
    return render(request, 'index.html', {'box': box})


def login_view(request):
    logout(request)
    if request.POST:
        username = request.POST.get('Login')
        password = request.POST.get('Password')
        print(username)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
    return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    url = reverse('index')
    return HttpResponseRedirect(url + '?message=logout')


def register_view(request):
    if request.POST:
        username = request.POST.get('Login')
        password = request.POST.get('Password')
        email = request.POST.get('Email')
        name = request.POST.get('Name')
        surname = request.POST.get('Surname')
        phone = request.POST.get('Phone')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email, password)
            site_user = SiteUser(user=user, name=name, surname=surname, phone_number=phone)
            site_user.save()
            return redirect('login')
    return render(request, 'register.html', {})


def user_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'user.html', {'userprofile': user.siteuser, 'user': user})
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .models import SiteUser, User, Offer
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
        street = request.POST.get('Street')
        postcode = request.POST.get('Postcode')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email, password)
            site_user = SiteUser(user=user, name=name, surname=surname, phone_number=phone, street=street,
                                 postcode=postcode)
            site_user.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'message': 'LOGINTAKEN'})
    return render(request, 'register.html', {})


def user_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'user.html', {'userprofile': user.siteuser, 'user': user})


def offer_view(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'offer.html', {'offer': offer})


def add_offer_view(request):
    if request.POST:
        title = request.POST.get('title')
        author = request.user
        category = request.POST.get('category')
        earliest_pickup = request.POST.get('earliest_pickup')
        latest_pickup = request.POST.get('latest_pickup')
        earliest_delivery = request.POST.get('earliest_delivery')
        latest_delivery = request.POST.get('latest_delivery')
        description = request.POST.get('description')
        length = request.POST.get('length')
        width = request.POST.get('width')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        price = request.POST.get('price')

        offer = Offer.objects.create(title=title, author=author, category=category, earliest_pickup=earliest_pickup,
                                     latest_pickup=latest_pickup, earliest_delivery=earliest_delivery,
                                     latest_delivery=latest_delivery, description=description, length=length,
                                     width=width, height=height, weight=weight, price_cap=price)
    return render(request, 'addoffer.html')

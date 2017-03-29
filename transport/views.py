from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .models import SiteUser, User, Offer, Conversation
from datetime import datetime
from .messages import get_conversation, get_messages, send_message, create_conversation
from django.db.models import Q
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
        date = datetime.now()
        author = request.user
        category = request.POST.get('category')
        earliest_pickup = request.POST.get('earliest_pickup')
        earliest_pickup = None if earliest_pickup == '' else earliest_pickup
        latest_pickup = request.POST.get('latest_pickup')
        latest_pickup = None if latest_pickup == '' else latest_pickup
        earliest_delivery = request.POST.get('earliest_delivery')
        earliest_delivery = None if earliest_delivery == '' else earliest_delivery
        latest_delivery = request.POST.get('latest_delivery')
        latest_delivery = None if latest_delivery == '' else latest_delivery
        description = request.POST.get('description')
        length = request.POST.get('length')
        length = None if length == '' else length
        width = request.POST.get('width')
        width = None if width == '' else width
        height = request.POST.get('height')
        height = None if height == '' else height
        weight = request.POST.get('weight')
        weight = None if weight == '' else weight
        price = request.POST.get('price')

        offer = Offer.objects.create(title=title, creation_date=date, author=author, category=category, earliest_pickup=earliest_pickup,
                                     latest_pickup=latest_pickup, earliest_delivery=earliest_delivery,
                                     latest_delivery=latest_delivery, description=description, length=length,
                                     width=width, height=height, weight=weight, price_cap=price)
    return render(request, 'addoffer.html')


def offers_list_view(request):
    if request.GET:
        title = request.GET.get('title')
        length = request.GET.get('length')
        width = request.GET.get('width')
        height = request.GET.get('height')
        weight = request.GET.get('weight')
        min_price = request.GET.get('min_price')
        queryset = Offer.objects.all()
        if title is not None:
            queryset = queryset.filter(title__contains=title)
        if length is not None:
            queryset = queryset.filter(length__lte=length)
        if width is not None:
            queryset = queryset.filter(width__lte=width)
        if height is not None:
            queryset = queryset.filter(height__lte=height)
        if weight is not None:
            queryset = queryset.filter(weight__lte=weight)
        if min_price is not None:
            queryset = queryset.filter(price_cap__gte=min_price)
        newest_offers = queryset.order_by('-creation_date')[0:20]
    else:
        newest_offers = Offer.objects.order_by('-creation_date')[0:20]
    return render(request, 'offerslist.html', {'newest_offers': newest_offers})


def conversation_view(request, username):
    user2 = get_object_or_404(User, username=username)
    conversation = get_conversation(request.user, user2)
    if request.POST:
        text = request.POST.get('message')
        send_message(conversation, request.user, text)

    if conversation is None:
        create_conversation(request.user, user2)
        conversation = get_conversation(request.user, user2)

    messages = get_messages(conversation, 10, 0)
    other_user = conversation.get_other_user(request.user).username
    return render(request, 'conversation.html', {'messages': messages, 'other_user': other_user})


def inbox_view(request):
    conversations = Conversation.objects.filter(users=request.user).exclude(messages=None)\
                    .order_by('-last_message_date')[0:20]
    senders = []
    for c in conversations:
        senders.append(c.get_other_user(request.user))
    zipped = zip(conversations, senders)
    return render(request, 'inbox.html', {'conversations': zipped})

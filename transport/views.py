from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .models import SiteUser, User, Offer, Conversation, Company, Category, CargoType, Vehicle, OfferBid, Preferences, \
    OfferMatch
from datetime import datetime
from .messages import get_conversation, get_messages, send_message, create_conversation
from .maps import get_location_model
from .offer_matching import create_match
from .utilities import get_categories


# Create your views here.


def index(request):
    message = request.GET.get('message')
    if message is not None:
        box = True
    else:
        box = False
    offers = Offer.objects.all()
    return render(request, 'index.html', {'box': box, 'offers': offers})


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
        city = request.POST.get('City')
        postcode = request.POST.get('Postcode')
        location = get_location_model(city, postcode)
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email, password)
            preferences = Preferences.objects.create()
            site_user = SiteUser(user=user, name=name, surname=surname, phone_number=phone, street=street,
                                 location=location, preferences=preferences)
            site_user.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'message': 'LOGINTAKEN'})
    return render(request, 'register.html', {})


def user_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'user.html', {'userprofile': user.siteuser, 'profile_user': user})


def offer_view(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)

    if request.POST:
        price = request.POST.get('price')
        bid = OfferBid.objects.create(offer=offer, user=request.user.siteuser, price=price)

    return render(request, 'offer.html', {'offer': offer})


def add_offer_view(request):
    if request.POST:
        title = request.POST.get('title')
        date = datetime.now()
        author = request.user
        category = request.POST.get('category')
        category = Category.objects.filter(pk=int(category))[0]
        earliest_pickup = request.POST.get('earliest_pickup')
        earliest_pickup = None if earliest_pickup == '' else earliest_pickup
        latest_pickup = request.POST.get('latest_pickup')
        latest_pickup = None if latest_pickup == '' else latest_pickup
        earliest_delivery = request.POST.get('earliest_delivery')
        earliest_delivery = None if earliest_delivery == '' else earliest_delivery
        latest_delivery = request.POST.get('latest_delivery')
        latest_delivery = None if latest_delivery == '' else latest_delivery
        description = request.POST.get('description')

        start_city = request.POST.get('start_city')
        start_postcode = request.POST.get('start_postcode')
        start_location = get_location_model(start_city, start_postcode)

        end_city = request.POST.get('end_city')
        end_postcode = request.POST.get('end_postcode')
        end_location = get_location_model(end_city, end_postcode)

        length = request.POST.get('length')
        length = None if length == '' else length
        width = request.POST.get('width')
        width = None if width == '' else width
        height = request.POST.get('height')
        height = None if height == '' else height
        weight = request.POST.get('weight')
        weight = None if weight == '' else weight
        price = request.POST.get('price')

        offer = Offer.objects.create(title=title, creation_date=date, author=author, category=category,
                                     earliest_pickup=earliest_pickup,
                                     latest_pickup=latest_pickup, earliest_delivery=earliest_delivery,
                                     latest_delivery=latest_delivery, description=description, length=length,
                                     width=width, height=height, weight=weight, price_cap=price,
                                     start_location=start_location,
                                     end_location=end_location)
    categories = get_categories()
    return render(request, 'addoffer.html', {'categories': categories})


def offers_list_view(request):
    if request.GET:
        title = request.GET.get('title')
        length = request.GET.get('length')
        width = request.GET.get('width')
        height = request.GET.get('height')
        weight = request.GET.get('weight')
        min_price = request.GET.get('min_price')
        sort_type = request.GET.get('sort')
        category = request.GET.get('category')
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
        if category is not None and category is not '':
            queryset = queryset.filter(category=category)
        if sort_type is not None:
            if sort_type == 'match':
                for offer in queryset:
                    create_match(offer, request.user.siteuser)
                newest_offers = Offer.objects.raw('''SELECT o.*
                                                      FROM transport_offer AS o
                                                        JOIN transport_offermatch AS m ON o.id = m.offer_id
                                                      WHERE m.user_id = ''' + str(request.user.pk) + '''
                                                      ORDER BY -m.value;
                                                  ''')

            if sort_type == 'latest':
                sort_type = '-creation_date'
            if sort_type == 'price':
                sort_type = 'price_cap'
        if sort_type != 'match':
            newest_offers = queryset.order_by(sort_type)[0:20]
    else:
        newest_offers = Offer.objects.order_by('-creation_date')[0:20]
    categories = get_categories()
    return render(request, 'offerslist.html', {'newest_offers': newest_offers, 'categories': categories})


def conversation_view(request, username):
    if username == request.user.username:
        return redirect('index')
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
    conversations = Conversation.objects.filter(users=request.user).exclude(messages=None) \
                        .order_by('-last_message_date')[0:20]
    senders = []
    for c in conversations:
        senders.append(c.get_other_user(request.user))
    zipped = zip(conversations, senders)
    return render(request, 'inbox.html', {'conversations': zipped})


def company_view(request):
    if request.user.siteuser.company is None:
        return redirect('create_company')
    company = get_object_or_404(Company, pk=request.user.siteuser.company.pk)
    if request.GET:
        remove = request.GET.get('remove')
        add = request.GET.get('add')
        if add is not None:
            user = get_object_or_404(User, username=add)
            user.siteuser.company = company
            user.siteuser.save()
        if remove is not None:
            user = get_object_or_404(User, username=remove)
            if user.siteuser.company == company:
                user.siteuser.company = None
                user.siteuser.save()
    return render(request, 'company.html', {'company': company})


def create_company_view(request):
    if request.POST:
        name = request.POST.get('Name')
        nip = request.POST.get('NIP')
        street = request.POST.get('Street')
        city = request.POST.get('City')
        postcode = request.POST.get('Postcode')
        location = get_location_model(city, postcode)
        owner = request.user.siteuser

        company = Company.objects.create(name=name, nip=nip, street=street, location=location, owner=owner)

        request.user.siteuser.company = company
        request.user.siteuser.save()
        return redirect('company')
    return render(request, 'createcompany.html', {})


def add_vehicle_view(request):
    if request.POST:
        model = request.POST.get('model')
        cargo_type = CargoType.objects.filter(pk=int(request.POST.get('cargo_type')))[0]
        max_capacity = request.POST.get('max_capacity')
        length = request.POST.get('length')
        width = request.POST.get('width')
        height = request.POST.get('height')
        owner = request.user.siteuser

        vehicle = Vehicle.objects.create(model=model, cargo_type=cargo_type, max_capacity=max_capacity, length=length,
                                         width=width, height=height, owner=owner)

        return redirect('index')
    cargo_types = CargoType.objects.all()
    cargo_types = zip([cat.pk for cat in cargo_types], [cat.name for cat in cargo_types])
    return render(request, 'addvehicle.html', {'cargo_types': cargo_types})


def vehicle_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    return render(request, 'vehicle.html', {'vehicle': vehicle})


def my_offers(request):
    offers = request.user.offers.all()

    if request.POST:
        bid_id = request.POST.get('id')
        bid = OfferBid.objects.get(pk=bid_id)
        bid.taken = True
        bid.save()

    return render(request, 'myoffers.html', {'offers': offers})


def search_preferences(request):
    preferences = request.user.siteuser.preferences

    if request.POST:
        dist = request.POST.get('distance')
        weight = request.POST.get('weight')
        dimensions = request.POST.get('dimensions')

        preferences.distance_to_start = dist
        preferences.cargo_weight = weight
        preferences.cargo_dimension = dimensions

        preferences.save()
        OfferMatch.objects.filter(user=request.user.siteuser).delete()

    return render(request, 'preferences.html', {'prefs': preferences})

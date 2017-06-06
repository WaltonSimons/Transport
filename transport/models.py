from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
import geocoder


# Create your models here.


class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=255)
    surname = models.TextField(max_length=255)
    phone_number = models.TextField(max_length=15, blank=True, null=True)
    company = models.ForeignKey('Company', related_name='employees', blank=True, null=True)
    street = models.TextField(max_length=255, blank=True, null=True)
    location = models.ForeignKey('Location', blank=True, null=True)
    preferences = models.ForeignKey('Preferences', blank=True, null=True)

    def formatted_postcode(self):
        return str(self.location.postcode)[0:2] + '-' + str(self.location.postcode)[2:5]

    def has_company(self):
        return self.company is not None

    def has_vehicle(self):
        return len(self.vehicles.all()) > 0


class Preferences(models.Model):
    distance_to_start = models.FloatField(default=1)
    cargo_weight = models.FloatField(default=1)
    cargo_dimension = models.FloatField(default=1)


class Company(models.Model):
    name = models.TextField(max_length=255)
    nip = models.IntegerField()
    street = models.TextField(max_length=255, blank=True, null=True)
    location = models.ForeignKey('Location', blank=True, null=True)
    owner = models.ForeignKey('SiteUser', related_name='owned_company', blank=True, null=True)


class Vehicle(models.Model):
    model = models.TextField(max_length=255, blank=True, null=True)
    cargo_type = models.ForeignKey('CargoType', blank=True, null=True)
    max_capacity = models.FloatField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey('SiteUser', related_name='vehicles')


class CargoType(models.Model):
    name = models.TextField(max_length=255)


class Location(models.Model):
    name = models.TextField(max_length=255, primary_key=True)
    postcode = models.TextField(max_length=5)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = (("name", "postcode"),)


class Offer(models.Model):
    creation_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='offers', null=True)
    title = models.TextField(max_length=512)
    description = models.TextField(max_length=5000)
    earliest_pickup = models.DateTimeField(default=timezone.now, blank=True, null=True)
    earliest_delivery = models.DateTimeField(default=timezone.now, blank=True, null=True)
    latest_pickup = models.DateTimeField(default=timezone.now, blank=True, null=True)
    latest_delivery = models.DateTimeField(default=timezone.now, blank=True, null=True)
    category = models.ForeignKey('Category')
    length = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    cargo_types = models.ManyToManyField('CargoType', related_name='offers')
    services = models.ManyToManyField('Service', related_name='offers')
    price_cap = models.IntegerField(blank=True, null=True)
    start_location = models.ForeignKey(Location, blank=True, null=True, related_name='offers_start')
    end_location = models.ForeignKey(Location, blank=True, null=True, related_name='offers_end')
    status = models.ForeignKey('OfferStatus', blank=True, null=True)

    def get_distance(self):
        location1 = self.start_location
        location2 = self.end_location
        coord1 = [location1.latitude, location1.longitude]
        coord2 = [location2.latitude, location2.longitude]
        return round(geocoder.distance(coord1, coord2), 1)

    def formatted_start_postcode(self):
        return str(self.start_location.postcode)[0:2] + '-' + str(self.start_location.postcode)[2:5]

    def formatted_end_postcode(self):
        return str(self.end_location.postcode)[0:2] + '-' + str(self.end_location.postcode)[2:5]

    def has_ended(self):
        for bid in self.bids.all():
            if bid.taken:
                return True
        return False


class OfferStatus(models.Model):
    name = models.TextField(max_length=255, blank=True, null=True)


class Service(models.Model):
    name = models.TextField(max_length=512, blank=True, null=True)


class Category(models.Model):
    name = models.TextField(max_length=512)
    parentCategory = models.ForeignKey('Category', blank=True, null=True)


class UserRating(models.Model):
    value = models.IntegerField()
    ratedUser = models.ForeignKey('SiteUser', related_name='received_ratings')
    ratingUser = models.ForeignKey('SiteUser', related_name='given_ratings')


class OfferMatch(models.Model):
    user = models.ForeignKey('SiteUser')
    offer = models.ForeignKey('Offer')
    value = models.FloatField()

    @staticmethod
    def reset_matches(user):
        OfferMatch.objects.filter(user=user.siteuser).delete()


class OfferBid(models.Model):
    offer = models.ForeignKey('Offer', related_name='bids')
    user = models.ForeignKey('SiteUser', related_name='bidded')
    price = models.IntegerField()
    taken = models.BooleanField(default=False)


class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name='conversations')
    last_message_date = models.DateTimeField(default=timezone.now)

    def last_message_short(self):
        last_message = self.messages.order_by('-creation_date')[0].text
        return last_message[:50] + '...' if len(last_message) > 50 else last_message

    def get_other_user(self, user):
        result = None
        for u in self.users.all():
            if u.username != user.username:
                result = u
        return result


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages')
    sender = models.ForeignKey(User, related_name='sender')
    text = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(default=timezone.now)

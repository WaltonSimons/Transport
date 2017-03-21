from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=255)
    surname = models.TextField(max_length=255)
    phone_number = models.TextField(max_length=15, blank=True, null=True)
    company = models.OneToOneField('Company', blank=True, null=True)
    street = models.TextField(max_length=255, blank=True, null=True)
    postcode = models.IntegerField(blank=True, null=True)
    city = models.ForeignKey('City', blank=True, null=True)

    def formatted_postcode(self):
        return str(self.postcode)[0:2] + '-' + str(self.postcode)[2:5]


class Company(models.Model):
    name = models.TextField(max_length=255)
    nip = models.IntegerField()
    street = models.TextField(max_length=255, blank=True, null=True)
    postcode = models.IntegerField(blank=True, null=True)
    city = models.ForeignKey('City', blank=True, null=True)


class City(models.Model):
    name = models.TextField(max_length=255, primary_key=True)


class Offer(models.Model):
    creation_date = models.DateTimeField(default=datetime.now())
    title = models.TextField(max_length=512)
    description = models.TextField(max_length=5000)
    earliest_pickup = models.DateTimeField(default=datetime.now(), blank=True, null=True)
    earliest_delivery = models.DateTimeField(default=datetime.now(), blank=True, null=True)
    latest_pickup = models.DateTimeField(default=datetime.now(), blank=True, null=True)
    latest_delivery = models.DateTimeField(default=datetime.now(), blank=True, null=True)
    category = models.TextField(max_length=255, blank=True, null=True) #TODO: Dodać model 'Category'
    length = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    price_cap = models.IntegerField(blank=True, null=True)


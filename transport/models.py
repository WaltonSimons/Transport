from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=255)
    surname = models.TextField(max_length=255)
    phone_number = models.TextField(max_length=15)


#    company = models.OneToOneField(Company, on_delete=models.CASCADE(), blank=True, null=True)
#    street = models.TextField(max_length=255)
#    postcode = models.IntegerField(max_length=5)
#    city = models.OneToOneField()
#
#
#class Company(models.Model):
#    name = models.TextField(max_length=255)
#    nip = models.IntegerField(max_length=10)
#
#
#class City(models.Model):
#    name = models.TextField(max_length=255)

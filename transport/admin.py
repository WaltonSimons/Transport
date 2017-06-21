from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(SiteUser)
admin.site.register(Conversation)
admin.site.register(Offer)
admin.site.register(Location)
admin.site.register(Preferences)
admin.site.register(Company)
admin.site.register(Vehicle)
admin.site.register(CargoType)
admin.site.register(Category)
admin.site.register(UserRating)
admin.site.register(OfferMatch)
admin.site.register(OfferBid)
admin.site.register(Message)
admin.site.register(Filter)

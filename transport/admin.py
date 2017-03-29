from django.contrib import admin
from .models import SiteUser, Conversation, Offer

# Register your models here.

admin.site.register(SiteUser)
admin.site.register(Conversation)
admin.site.register(Offer)
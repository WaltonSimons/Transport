from django.contrib import admin
from .models import SiteUser, Conversation

# Register your models here.

admin.site.register(SiteUser)
admin.site.register(Conversation)
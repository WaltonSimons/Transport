from django.shortcuts import get_object_or_404
from .models import SiteUser, User, Message, Conversation
from datetime import datetime


def create_conversation(user1, user2):
    conversation = Conversation()
    conversation.save()
    conversation.users.add(user1)
    conversation.users.add(user2)


def get_conversation(user1, user2):
    result = Conversation.objects.filter(users=user1).filter(users=user2)
    return result[0] if len(result) != 0 else None


def get_messages(conversation, number, offset):
    return conversation.messages.order_by('creation_date')[offset:offset+number]


def send_message(conversation, sender, text):
    text = text[:5000] if len(text) > 5000 else text
    date = datetime.now()
    message = Message.objects.create(conversation=conversation, sender=sender, text=text, creation_date=date)
    conversation.last_message_date = date

from django.conf.urls import url
from django.contrib.auth import views as authviews

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login/', views.login_view, name='login'),
    url(r'logout/', views.logout_view, name='logout'),
    url(r'register/', views.register_view, name='register'),
    url(r'user/(?P<username>[\w\-]+)/', views.user_view, name='user'),
    url(r'offer/(?P<offer_id>\d+)/', views.offer_view, name='offer'),
    url(r'addoffer/', views.add_offer_view, name='add_offer'),
    url(r'browse/', views.offers_list_view, name='offers_list'),
    url(r'inbox/(?P<username>[\w\-]+)/', views.conversation_view, name='conversation'),
    url(r'inbox/', views.inbox_view, name='inbox'),
    url(r'createcompany/', views.create_company_view, name='create_company'),
    url(r'company/', views.company_view, name='company'),
    url(r'addvehicle/', views.add_vehicle_view, name='add_vehicle'),
    url(r'vehicle/(?P<vehicle_id>\d+)/', views.vehicle_view, name='vehicle'),
    url(r'myoffers/', views.my_offers, name='my_offers'),
    url(r'preferences', views.search_preferences, name='search_preferences'),
]

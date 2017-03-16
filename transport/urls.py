from django.conf.urls import url
from django.contrib.auth import views as authviews

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login/', views.login_view, name='login'),
    url(r'logout/', views.logout_view, name='logout'),
    url(r'register/', views.register_view, name='register'),
    url(r'user/(?P<username>[\w\-]+)/', views.user_view, name='user')
]
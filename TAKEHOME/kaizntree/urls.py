from django.contrib import admin
from django.urls import path, include
from . import views
from .views import item_dashboard

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('item_dashboard', item_dashboard.as_view(), name='item_dashboard'),
]
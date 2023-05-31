from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.spotify_login, name="login"),
    path("callback", views.callback, name="callback"),
    path("home", views.home, name="home"),
]
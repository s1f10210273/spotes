from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.spotify_login, name="login"),
    path("logout", views.spotify_logout, name="logout"),
    path("callback/", views.callback, name="callback"),
    path("home", views.home, name="home"),
    path("play/", views.play, name="play"),
]
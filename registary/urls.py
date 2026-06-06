from django.urls import path
from .views import home_view, register_view

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register_view, name="register")
]
from django.contrib import admin
from django.urls import path, include 
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

from .views import home_view, register_view, profile


def redirect_to_login(request):
    return redirect('login')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("profile/", profile, name="profile"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html", next_page="login.html"), name="logout")
]
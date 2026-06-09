from django.contrib import admin
from django.urls import path, include 
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

from .views import (
    home_view, register_view, profile, profile_edit,
    search_view, admin_dashboard, update_user_limits, update_global_limits
)


def redirect_to_login(request):
    return redirect('login')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    path("login/", auth_views.LoginView.as_view(template_name="registary/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="registary/logout.html"), name="logout"),
    path("search/", search_view, name="search"),
]
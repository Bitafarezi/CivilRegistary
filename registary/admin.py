from django.contrib import admin
from .models import UserProfile, Citizen, GlobalSettings

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'daily_usage', 'daily_limit', 'monthly_usage', 'monthly_limit')
    search_fields = ('user__username',)

@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'national_id', 'phone_number')
    search_fields = ('first_name', 'last_name', 'national_id', 'phone_number')
    ordering = ('first_name',)

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('default_daily_limit', 'default_monthly_limit')

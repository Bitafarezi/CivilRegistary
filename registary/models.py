from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Citizen(models.Model):
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    national_id = models.CharField(max_length=10, unique=True, db_index=True)
    phone_number = models.CharField(max_length=15, db_index=True) # Format: +989121111111
    father_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    address = models.TextField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    citizen = models.OneToOneField(Citizen, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')
    # Consumption fields
    daily_limit = models.PositiveIntegerField(default=10)
    monthly_limit = models.PositiveIntegerField(default=100)
    daily_usage = models.PositiveIntegerField(default=0)
    monthly_usage = models.PositiveIntegerField(default=0)
    last_usage_reset = models.DateTimeField(default=timezone.now)
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def reset_usage_if_needed(self):
        now = timezone.now()
        if self.last_usage_reset.date() < now.date():
            self.daily_usage = 0
            if self.last_usage_reset.month < now.month or self.last_usage_reset.year < now.year:
                self.monthly_usage = 0
            self.last_usage_reset = now
            self.save()


class GlobalSettings(models.Model):
    default_daily_limit = models.PositiveIntegerField(default=10)
    default_monthly_limit = models.PositiveIntegerField(default=100)

    class Meta:
        verbose_name_plural = "Global Settings"

    def __str__(self):
        return "Global Settings"

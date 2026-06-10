from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, GlobalSettings

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        global_settings = GlobalSettings.objects.first()
        daily = 10
        monthly = 100
        if global_settings:
            daily = global_settings.default_daily_limit
            monthly = global_settings.default_monthly_limit
        
        UserProfile.objects.create(
            user=instance,
            daily_limit=daily,
            monthly_limit=monthly
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

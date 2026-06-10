from django.contrib.auth.models import User
from registary.models import UserProfile, GlobalSettings

def run():
    gs = GlobalSettings.objects.first()
    daily = gs.default_daily_limit if gs else 10
    monthly = gs.default_monthly_limit if gs else 100
    
    for u in User.objects.all():
        if not hasattr(u, 'profile'):
            UserProfile.objects.create(user=u, daily_limit=daily, monthly_limit=monthly)
            print(f'Created profile for {u.username}')
        else:
            print(f'Profile already exists for {u.username}')

if __name__ == "__main__":
    run()

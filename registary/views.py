import time
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserRegistrationForm, UserUpdateForm
from .models import Citizen, UserProfile, GlobalSettings


@login_required
def home_view(request):
    return render(request, 'registary/home.html')

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account was created for {username}!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registary/register.html', {'form': form})

@login_required
def search_view(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    user_profile.reset_usage_if_needed()

    if user_profile.daily_usage >= user_profile.daily_limit:
        messages.error(request, "Daily search limit reached.")
        return render(request, 'registary/search.html', {'limit_reached': True})
    
    if user_profile.monthly_usage >= user_profile.monthly_limit:
        messages.error(request, "Monthly search limit reached.")
        return render(request, 'registary/search.html', {'limit_reached': True})

    query = request.GET.get('q', '')
    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')
    national_id = request.GET.get('national_id', '')
    phone_number = request.GET.get('phone_number', '')

    results = []
    duration = 0
    count = 0

    if query or first_name or last_name or national_id or phone_number:
        start_time = time.time()
        
        # Base queryset
        queryset = Citizen.objects.all()

        # Global search
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(national_id__icontains=query) |
                Q(phone_number__icontains=query)
            )
        
        # Specific filters
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if national_id:
            queryset = queryset.filter(national_id__icontains=national_id)
        if phone_number:
            queryset = queryset.filter(phone_number__icontains=phone_number)
        
        results = queryset[:50] 
        count = queryset.count()
        
        duration = time.time() - start_time
        
        # Increment consumption
        user_profile.daily_usage += 1
        user_profile.monthly_usage += 1
        user_profile.save()

    context = {
        'results': results,
        'query': query,
        'duration': round(duration, 4),
        'count': count,
        'user_profile': user_profile,
    }
    return render(request, 'registary/search.html', context)

@login_required
def profile(request):
    return render(request, 'registary/profile.html')

@login_required
def profile_edit(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'registary/profile_edit.html', {'form': form})
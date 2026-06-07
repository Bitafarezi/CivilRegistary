from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

# Create your views here.

def home_view(request):
    return render(request, 'home.html')

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
        
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html')
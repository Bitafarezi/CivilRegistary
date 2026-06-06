from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
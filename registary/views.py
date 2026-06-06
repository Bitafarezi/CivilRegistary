from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    return render(request, 'templates/home.html')

def register_view(request):
    form = UserCreationForm()
    return render(request, 'templates/register.html', {'form': form})
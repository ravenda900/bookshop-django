from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def home(request):
    return render(request, 'home.html', {
        'books': Book.objects.all()
    })

def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.age = form.cleaned_data.get('age')
        user.profile.address_barangay = form.cleaned_data.get('address_barangay')
        user.profile.address_street = form.cleaned_data.get('address_street')
        user.profile.address_city = form.cleaned_data.get('address_city')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


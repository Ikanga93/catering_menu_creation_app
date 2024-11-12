
# menu_management/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import logout as auth_logout

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash the password
            user.save()
            login(request, user)  # Automatically log in the user after registration
            return JsonResponse({"message": "Registration successful", "user": user.username})
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({"message": "Login successful", "user": user.username})
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form})
# Logout View
@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("login")

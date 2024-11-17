from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import (
    CustomLoginForm,
    CustomSignupForm,
    ProfileForm,
    UserUpdateForm,
)


# Profile Update View
@login_required
def profile_view(request):
    profile = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, user + ', Your account has been created.')
            return redirect('accounts:account_login')
    else:
        messages.error(request, "Please fill out all fields")
        return render(request, 'accounts/signup.html', {'form': form})
    
form = CustomSignupForm()


# Login View
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, username + ', you are successfully logged in!')
            if user.is_superuser:
                return HttpResponseRedirect('../admin/')
            else:
                messages.error(request, "Invalid username or password! Try again")
                return redirect('login_view')
    else:
        form = CustomLoginForm()
        return render(request, 'accounts/login.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import (
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
    form = CustomSignupForm()
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data('username')
            password = form.cleaned_data('password1')
            # log in user
            user = authenticate (username=username, password=password)
            login(request, user)
            messages.success(request, ("Your account has been created."))
            return redirect('home')
        else:
            messages.error(request, ("There was a problem registering, please try again."))
            return redirect('account_signup')
    else:
        return render(request, 'accounts/signup.html', {'form': form})
    

# Login View
def login_view(request):
    if request.method == 'POST':
            email = request.POST('email')
            password = request.POST('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
                
            else:
                return redirect('login')
    else:
        return render(request, 'accounts/login.html', {})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomSignupForm,
    UpdateProfileForm,
    PasswordChangeForm,
)


# Profile Update View
@login_required
def update_profile_view(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateProfileForm(
                request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            current_user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, current_user)
            messages.success(request, "Woho!! Your Profile has been updated!!")
            return redirect('home')

        return render(
                request, 'accounts/userprofile_update.html', {
                        'user_form': user_form})
    else:
        messages.success(request, "Please log in to view this page.!!")
        return redirect('home')


# password update
def password_update_view(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = PasswordChangeForm(current_user, request.POST)

            if form.is_valid():
                form.save()

                current_user.backend = 'django.contrib.auth.backends.ModelBackend'

                messages.success(request, "Your Password Has Been Updated")
                login(request, current_user)

                return redirect('accounts:userprofile_update')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

                return redirect('accounts:password_update')
        else:
            form = PasswordChangeForm(current_user)
            return render(request, "accounts/password_update.html", {'form': form})

    else:
        messages.error(request, "Please log in to view this page!")
        return redirect('home')


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
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Your account has been created."))
            return redirect('home')
        else:
            messages.error(request, ("There was a problem registering, try again."))
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

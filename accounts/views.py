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
    """
    View to handle profile updates for authenticated users.
    If the user is logged in, the form to update the profile is displayed and saved.
    Displays success or error messages based on the form submission result.
    
    Returns:
        - A redirect to 'home' if the form is valid and the profile is updated.
        - A rendered profile update form if there are errors.
        - A redirect to 'home' if the user is not authenticated.
    """
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
    """
    View to handle password updates for authenticated users.
    If the user is logged in, the form to update the password is displayed and saved.
    Displays success or error messages based on the form submission result.
    
    Returns:
        - A redirect to the password update page on error.
        - A redirect to the user profile update page on success.
        - A redirect to 'home' if the user is not authenticated.
    """
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
    """
    View to handle user sign-up.
    Displays a form for users to sign up, and logs them in if registration is successful.
    Displays an error message if registration fails.
    
    Returns:
        - A redirect to 'home' after successful sign-up and login.
        - A redirect to the sign-up page if there is an error in registration.
        - A rendered sign-up form on a GET request.
    """
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
    """
    View to handle user login.
    Authenticates the user based on provided credentials and logs them in.
    Redirects to 'home' on successful login, or back to login on failure.
    
    Returns:
        - A redirect to 'home' if login is successful.
        - A redirect back to the login page if login fails.
        - A rendered login form on a GET request.
    """
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

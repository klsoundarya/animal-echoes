from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from allauth.account.views import SignupView

class CustomSignupView(SignupView):
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Thank you for registering, {username}! Please log in to continue.")
        return redirect('account_login') 

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'{request.user.username}, Your profile is updated.')
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ProfileForm(instance=profile)
        return render(request, 'accounts/profile.html', {'form': form})


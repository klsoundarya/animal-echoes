# accounts/forms.py
from django import forms
from .models import Profile
from allauth.account.forms import SignupForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'profile_image', 'title', 'birth_date']

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].label = "Email"
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})

        self.fields['password1'].label = "Password"
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})

        self.fields['password2'].label = "Repeat Password"
        self.fields['password2'].widget.attrs.update({'placeholder': '*** Repeat Password ***'})

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        return user
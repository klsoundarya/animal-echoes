# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from .models import Profile


# signup form
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=180, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=200, required=True)
    username = forms.CharField(max_length=150, required=True, help_text='Required. 150 characters or fewer.')

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].label = "Email"
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})

        self.fields['username'].label = "Username"
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})

        self.fields['first_name'].label = "First Name"
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})


        self.fields['last_name'].label = "Last Name"
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})

        self.fields['password1'].label = "Password"
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})

        self.fields['password2'].label = "Repeat Password"
        self.fields['password2'].widget.attrs.update({'placeholder': '****Repeat Password****'})

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        return user
        

# Profile Update Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'profile_image', 'title', 'birth_date']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


# User Update Form for updating user 

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

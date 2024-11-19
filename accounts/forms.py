# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserChangeForm, SetPasswordForm

# Password Update Form
class PasswordChangeForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(PasswordChangeForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


# Profile Update Form
class UpdateProfileForm(UserChangeForm):
    # Hide password field
    password = None

    first_name = forms.CharField(max_length=180, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=200, required=True)
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Required. 150 characters or fewer.'
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email"
        ]

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = "Email"
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})

        self.fields['username'].label = "Username"
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})

        self.fields['first_name'].label = "First Name"
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})


        self.fields['last_name'].label = "Last Name"
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})




# signup form
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=180, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=200, required=True)
    username = forms.CharField(max_length=150, required=True, help_text='Required. 150 characters or fewer.')

    class Meta:
        model = User
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
        
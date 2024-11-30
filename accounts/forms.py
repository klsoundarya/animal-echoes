# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserChangeForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class PasswordChangeForm(SetPasswordForm):
    """
    Form to handle password change for the user.
    Validates the new password according to specific criteria and updates the user's password.
    Fields:
        - new_password1: The new password.
        - new_password2: Confirmation of the new password.
    """
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = (
            "<ul>"
            "<li>Your password can’t be too similar to your other personal information.</li>"
            "<li>Your password must contain at least 8 characters.</li>"
            "<li>Your password can’t be a commonly used password.</li>"
            "<li>Your password can’t be entirely numeric.</li>"
            "</ul>"
        )

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = (
            "<ul><li>Enter the same password as before, for verification.</li></ul>"

        )


# Profile Update Form
class UpdateProfileForm(UserChangeForm):
    """
    Form to update user profile details (first name, last name, username, and email).
    Password field is excluded from this form as it's not intended for password changes.

    Fields:
        - username: The username of the user.
        - first_name: The user's first name.
        - last_name: The user's last name.
        - email: The user's email address.
    """
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
        """
        Initializes the UpdateProfileForm with customized widgets and labels for better user experience.
        """
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
    """
    Custom signup form that extends the default allauth signup form to include first name, last name,
    and email fields. It also validates passwords with custom rules and ensures password confirmation.

    Fields:
        - username: The desired username.
        - first_name: The user's first name.
        - last_name: The user's last name.
        - email: The user's email address.
        - password1: The user's password.
        - password2: The confirmation for the password.
    """
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
        self.fields['password1'].help_text = (
            "<ul>"
            "<li>Your password can’t be too similar to your other personal information.</li>"
            "<li>Your password must contain at least 8 characters.</li>"
            "<li>Your password can’t be a commonly used password.</li>"
            "<li>Your password can’t be entirely numeric.</li>"
            "</ul>"
        )

        self.fields['password2'].label = "Repeat Password"
        self.fields['password2'].widget.attrs.update({'placeholder': '****Repeat Password****'})
        self.fields['password2'].help_text = "<ul><li>Enter the same password as before, for verification.</li></ul>"

    # Custom validation for password confirmation
    def clean_password2(self):
        """
        Validates that the two password fields match. Raises a ValidationError if they do not match.
        Returns:
            - The cleaned password2 if both passwords match.
            - Raises ValidationError if passwords do not match.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("The two password fields must match."))
        return password2

    # Custom validation for password strength
    def clean_password1(self):
        """
        Validates that the password is at least 8 characters long.
        Returns:
            - The cleaned password1 if it meets the criteria.
            - Raises ValidationError if the password is shorter than 8 characters.
        """
        password = self.cleaned_data.get('password1')
        if password and len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))
        return password

    def save(self, request):
        """
        Saves the user object after successful validation of the signup form.

        Args:
            request: The HTTP request object.

        Returns:
            - The created user instance after saving.
        """
        user = super(CustomSignupForm, self).save(request)
        return user

from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'subject', 'message']

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
        )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
        )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'name@example.com'})
        )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter subject'})
        )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': '.......'})
        )

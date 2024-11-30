from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from .models import Contact
from .forms import ContactForm

# Contact form handling view


def contact(request):
    """
    Handles contact form submissions and displays submitted messages for superusers.

    - If the form is submitted (POST) and valid, it saves the data and displays a success message.
    - Redirects back to the contact page after successful submission.
    - If the user is a superuser, retrieves all submitted contact messages in descending order of creation.
    - Renders the 'contact/contact.html' template with the form and contact messages (for superusers).
    """
    form = ContactForm(request.POST or None)  # Instantiate form with POST data if available
    contacts = None  # Initialize contacts as None

    if request.method == "POST":
        if form.is_valid():
            form.save() # Save valid form data
            messages.success(
                request,
                "I’ll respond within 2 working days."
                "Thank you for submitting the form!")
            return redirect('contact')  # Redirect to the same page


    if request.user.is_superuser:
        contacts = Contact.objects.all().order_by('-created_at')  # Fetch all messages for superusers

    return render(
        request, 'contact/contact.html', {'form': form, 'contacts': contacts})

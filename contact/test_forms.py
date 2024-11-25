from django.test import TestCase
from .forms import ContactForm


class TestContactForm(TestCase):

    def test_form_is_valid(self):
        """ Test for all fields"""
        form = ContactForm({
            'first_name': 'john',
            'last_name': 'burris',
            'email': 'test@example.com',
            'subject':'would want to get email update',
            'message': 'Hello!'
        })
        self.assertTrue(form.is_valid(), msg="ContactForm form should be valid with all fields.")

    def test_form_is_invalid(self):
        """ Test for all fields"""
        form = ContactForm({
            'first_name': '',
            'last_name': '',
            'email': '',
            'subject':'',
            'message': ''
        })
        self.assertFalse(form.is_valid(), msg="ContactForm form should be invalid when all fields are empty.")

    def test_first_name_is_required(self):
        """Test for the 'name' field"""
        form = ContactForm({
            'first_name': '',
            'last_name': 'burris',
            'email': 'test@example.com',
            'subject':'would want to get email update',
            'message': 'Hello!'
        })
        self.assertFalse(
            form.is_valid(),
            msg="First Name was not provided, but the form is valid"
        )
    
    def test_last_name_is_required(self):
        """Test for the 'name' field"""
        form = ContactForm({
            'first_name': 'john',
            'last_name': '',
            'email': 'test@example.com',
            'subject':'would want to get email update',
            'message': 'Hello!'
        })
        self.assertFalse(
            form.is_valid(),
            msg="last Name was not provided, but the form is valid"
        )

    def test_email_is_required(self):
        """Test for the 'email' field"""
        form = ContactForm({
            'first_name': 'john',
            'last_name': 'burris',
            'email': '',
            'subject':'would want to get email update',
            'message': 'Hello!'
        })
        self.assertFalse(
            form.is_valid(),
            msg="Email was not provided, but the form is valid"
        )

    def test_subject_is_required(self):
        """Test for the 'message' field"""
        form = ContactForm({
            'first_name': 'john',
            'last_name': 'burris',
            'email': 'test@example.com',
            'subject':'',
            'message': 'Hello!'
        })
        self.assertFalse(
            form.is_valid(),
            msg="Subject was not provided, but the form is valid"
        )

    def test_message_is_required(self):
        """Test for the 'message' field"""
        form = ContactForm({
            'first_name': 'john',
            'last_name': 'burris',
            'email': 'test@example.com',
            'subject':'would want to get email update',
            'message': ''
        })
        self.assertFalse(
            form.is_valid(),
            msg="Message was not provided, but the form is valid"
        )
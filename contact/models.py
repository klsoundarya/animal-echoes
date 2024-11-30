from django.db import models
"""
    Model to store contact form submissions.

    Fields:
    - first_name: First name of the contact person (max length: 50).
    - last_name: Last name of the contact person (max length: 50).
    - email: Email address of the contact person (max length: 70).
    - subject: Subject of the message (max length: 80).
    - message: Content of the contact message.
    - created_at: Date and time when the contact message was created (auto set on creation).
    - read: Boolean flag indicating whether the message has been read by an admin (default is False).
"""

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    subject = models.CharField(max_length=80)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"

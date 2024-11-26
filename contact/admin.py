from django.contrib import admin
from .models import Contact

# contact-admin.py


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('message', 'email', 'read')
    list_editable = ('read',)
    search_fields = ('first_name', 'email')
    list_filter = ('created_at', 'first_name')

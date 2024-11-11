from django.contrib import admin
from .models import Contact

# contact-admin.py

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at')
    search_fields = ('first_name', 'email')
    list_filter = ('created_at',)

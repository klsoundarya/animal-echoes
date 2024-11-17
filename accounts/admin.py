from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'name', 'birth_date', 'updated_on')
    list_filter = ('title',)
    search_fields = ('user__username', 'name')

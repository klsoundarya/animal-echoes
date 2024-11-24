from django.contrib import admin
from .models import BlogPost, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(BlogPost)
class PostAdmin(SummernoteModelAdmin):
    """
    Lists fields for display in admin, fileds for search,
    field filters, fields to prepopulate and rich-text editor.
    """

    list_display = ('title', 'status', 'created_on', 'read')
    list_editable = ('read',)
    search_fields = ['title', 'content', 'read']
    list_filter = ('status', 'created_on', 'read')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fileds for search and
    field filters.
    """
        
    list_display = ('author', 'post', 'approved', 'created_on')
    list_filter = ('approved', 'created_on',)
    search_fields = ('author', 'body',)

    actions = ['approve_comments']




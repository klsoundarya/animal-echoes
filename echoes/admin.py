from django.contrib import admin
from .models import BlogPost, BlogPostImage, Tag, Comment, FunFactSlider, AnimalFact, GuestUser
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import format_html
from django.utils.timezone import now


@admin.register(GuestUser)
class GuestUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')


@admin.register(FunFactSlider)
class FunFactSliderAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'fact_text', 'created_at')
    search_fields = ('blog_post__title', 'fact_text')


@admin.register(AnimalFact)
class AnimalFactAdmin(admin.ModelAdmin):
    list_display = ('animal', 'fact_text')
    search_fields = ('animal__title', 'fact_text')
    


@admin.register(BlogPost)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'status', 'approve', 'created_on')
    list_editable = ('approve', 'status')
    search_fields = ['title', 'description']
    list_filter = ('status', 'date', 'approve')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('intro', 'description',)


class BlogPostImageInline(admin.StackedInline):
    model = BlogPostImage
    extra = 1


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'approved', 'created_on', 'approve_comment_action')
    list_filter = ('approved', 'created_on',)
    search_fields = ('author', 'body',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True, approved_on=now())  # Ensure 'approved_on' is updated
    approve_comments.short_description = 'Approve selected comments'

    def approve_comment_action(self, obj):
        if obj.approved:
            return format_html('<span style="color: green;">Approved</span>')
        return format_html('<span style="color: red;">Pending</span>')

    approve_comment_action.short_description = 'Approval Status'

admin.site.register(Tag)

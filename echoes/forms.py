from .models import BlogPost, Comment
from django import forms
from django.utils.text import slugify


class BlogPostForm(forms.ModelForm):
    """
    A form for creating and submitting blog post.
    """
    class Meta:
        model = BlogPost
        fields = ['title', 'featured_image', 'description', 'habitat', 'species', 'sound_cloudinary']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter name of the animal'}),
            'description': forms.Textarea(attrs={
                    'class': 'form-control', 'rows': 5, 'placeholder': 'Write your blog content here...'}),
            'habitat': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Write short on animal habitat'}),
            'species': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter species'}),
        }
        help_texts = {
        'featured_image': 'Upload an image file (e.g., JPG, PNG).',
        'sound_cloudinary': 'Upload an audio file (e.g., MP3, WAV).',
        }

    def clean_title(self):
        """
        Ensure the title is unique by checking the slug field
        """
        title = self.cleaned_data['title']
        slug = slugify(title)
        if BlogPost.objects.filter(slug=slug).exists():
            raise forms.ValidationError("A blog post with a similar title already exists. Please choose a different title.")
        return title


class CommentForm(forms.ModelForm):
    """
    Form class for users to comment on a post
    """
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment...'
            }),
        }

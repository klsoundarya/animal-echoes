from .models import BlogPost, Comment
from django import forms


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'featured_image', 'content', 'excerpt', 'sound_cloudinary']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title'}),
            'slug': forms.TextInput(attrs={'placeholder': 'Enter slug'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your blog content here...'}),
            'excerpt': forms.Textarea(attrs={'placeholder': 'Short summary of your blog'}),
        }


class CommentField(forms.ModelForm):
    """
    Form class for users to comment on a post 
    """
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment...'
            }),
        }
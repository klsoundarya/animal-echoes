from django.test import TestCase
from .forms import CommentForm, BlogPostForm
from .models import BlogPost
from django.contrib.auth.models import User


class TestCommentForm(TestCase):
    """Test cases for CommentForm."""

    def test_form_is_valid(self):
        """Check if the form is valid when body is provided."""
        form = CommentForm({'body': 'This is a valid comment'})
        self.assertTrue(form.is_valid(), msg="Comment form should be valid.")

    def test_form_is_invalid(self):
        """Check if the form is invalid when body is missing."""
        form = CommentForm({'body': ''})
        self.assertFalse(
            form.is_valid(), msg="Comment form should be invalid.")


class TestBlogPostForm(TestCase):
    """Test cases for BlogPostForm."""

    def test_form_is_valid(self):
        """Check if the form is valid with all required fields."""
        form = BlogPostForm({
            'title': 'Valid Title',
            'content': 'Content about animals',
            'excerpt': 'Short summary',
        })
        self.assertTrue(form.is_valid(), msg="BlogPost form should be valid with all fields.")

    def test_form_is_invalid_with_empty_title(self):
        """Check if the form is invalid when the title is missing."""
        form = BlogPostForm({
            'title': '',
            'content': 'Content about animals',
            'excerpt': 'Short summary',
        })
        self.assertFalse(form.is_valid(), msg="BlogPost form should be invalid without a title.")

    def test_form_is_invalid_with_empty_content(self):
        """Check if the form is invalid when content is missing."""
        form = BlogPostForm({
            'title': 'Valid Title',
            'content': '',
            'excerpt': 'Short summary',
        })
        self.assertFalse(form.is_valid(), msg="BlogPost form should be invalid without content.")

    def test_clean_title(self):
        user = User.objects.create_user(username='san', password='password123')
        BlogPost.objects.create(
            title="Cheetah: The Fastest Land Animal",
            slug="cheetah-the-fastest-land-animal",
            author=user,
            content="Some content for the blog post"
        )

        # valid and invalid title inputs
        form_data_valid = {
            'title': 'Echo of the Wild',
            'content': 'Some valid content for the post'
        }
        form_data_invalid = {
            'title': 'Cheetah: The Fastest Land Animal',
            'content': 'Some valid content for the post'
        }

        form_valid = BlogPostForm(data=form_data_valid)
        self.assertTrue(form_valid.is_valid(), msg="Form should pass validation")

        form_invalid = BlogPostForm(data=form_data_invalid)
        self.assertFalse(form_invalid.is_valid(), msg="Form should fail validation")
        self.assertIn('title', form_invalid.errors)

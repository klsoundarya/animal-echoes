from django.test import TestCase
from .forms import CommentForm, BlogPostForm
from .models import BlogPost
from django.contrib.auth.models import User


class TestCommentForm(TestCase):
    """Test cases for CommentForm."""

    def test_form_is_valid(self):
        """
        Test if the form is valid when the body is provided.

        - Expectation
        The form should be valid if the 'body' field is not empty.
        """
        form = CommentForm({'body': 'This is a valid comment'})
        self.assertTrue(form.is_valid(), msg="Comment form should be valid.")

    def test_form_is_invalid(self):
        """
        Test if the form is invalid when the body is missing.

        **Expectation**
        The form should be invalid if the 'body' field is empty.
        """
        form = CommentForm({'body': ''})
        self.assertFalse(
            form.is_valid(), msg="Comment form should be invalid.")


class TestBlogPostForm(TestCase):
    """Test cases for BlogPostForm."""

    def setUp(self):
        """
        Set up required data for the tests.

        This method runs before each test case to set up the necessary data, 
        including creating a user and a BlogPost instance with a duplicate title.
        """
        self.user = User.objects.create_user(
            username='san', password='password123'
        )
        BlogPost.objects.create(
            title="Duplicate Title",
            slug="duplicate-title",
            intro="Intro for duplicate title.",
            description="Description for duplicate title.",
            author=self.user,
        )

    def test_form_is_valid(self):
        """
        Test if the form is valid with all required fields.

        - Expectation
        The form should be valid if all required fields are filled, including title, slug, intro, 
        description, and status.
        """
        form_data = {
            "title": "Valid Blog Post",
            "slug": "valid-blog-post",
            "intro": "This is a valid intro.",
            "description": "This is a valid description.",
            "status": 1,  # Published
        }
        form = BlogPostForm(data=form_data)
        self.assertTrue(
            form.is_valid(), msg="BlogPost form should be valid with all fields."
        )

    def test_form_is_invalid_with_empty_title(self):
        """
        Test if the form is invalid when the title is missing.

        - Expectation
        The form should be invalid if the title field is empty.
        """
        form = BlogPostForm({
            'title': '',
            'description': 'Content about animals',
            'intro': 'Short summary',  # Fixed typo in 'intro '
        })
        self.assertFalse(
            form.is_valid(), msg="BlogPost form should be invalid without a title."
        )

    def test_form_is_invalid_with_empty_content(self):
        """
        Test if the form is invalid when content (description) is missing.

        - Expectation
        The form should be invalid if the description field is empty.
        """
        form = BlogPostForm({
            'title': 'Valid Title',
            'description': '',
            'intro': 'Short summary',  # Fixed typo in 'intro '
        })
        self.assertFalse(
            form.is_valid(), msg="BlogPost form should be invalid without content."
        )

    def test_clean_title(self):
        """
        Test the title validation logic in the form.

        - Expectation
        The form should be valid when the title is unique, and should fail validation if 
        the title already exists in the database.
        """
        # Valid title input
        form_data_valid = {
            'title': 'Unique Title',
            'description': 'Some valid content for the post',
        }
        form_valid = BlogPostForm(data=form_data_valid)
        self.assertTrue(
            form_valid.is_valid(), msg="Form should pass validation with a unique title."
        )

        # Invalid title input (duplicate title)
        form_data_invalid = {
            'title': 'Duplicate Title',  # Same title as in setUp
            'description': 'Some valid content for the post',
        }
        form_invalid = BlogPostForm(data=form_data_invalid)
        self.assertFalse(
            form_invalid.is_valid(), msg="Form should fail validation with a duplicate title."
        )
        self.assertIn('title', form_invalid.errors)
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CommentForm
from .models import BlogPost, Comment


class TestBlogViews(TestCase):
    """Test cases for Blog post views, including comment and like functionalities."""
    def setUp(self):
        """
        Set up test data for blog posts and comments.
        
        This method creates a superuser, a blog post, and an initial comment 
        to be used in various test cases.
        """
        self.user = User.objects.create_superuser(
            username="testUsername",
            password="myPassword123",
            email="test@test.com"
        )
        self.post = BlogPost.objects.create(
            title="Test Blog Post",
            slug="test-blog-post",
            intro="This is a test intro.",
            description="This is a test description for the blog post.",
            author=self.user,
            status=1,
        )
        self.post.save()
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Initial test comment"
        )

    def test_render_animal_detail_page_with_comment_form(self):
        """
        Test rendering the animal detail page with the comment form.

        - Expectation
        The page should load successfully, display the blog post's description, 
        and include a CommentForm in the context.
        """
        response = self.client.get(reverse('animal_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This is a test description for the blog post.", response.content)
        self.assertIsInstance(response.context['comment_form'], CommentForm)


    def test_successful_comment_submission(self):
        """
        Test for posting a comment on a blog post.

        - Expectation
        After logging in and submitting a valid comment, the user should be redirected 
        and receive a confirmation message indicating that the comment is awaiting approval.
        """
        logged_in = self.client.login(
            username="testUsername", password="myPassword123"
            )
        
        self.assertTrue(logged_in)

        post_data = {
            'body': 'This is a test comment.'
        }

        response = self.client.post(
            reverse('animal_detail', args=[self.post.slug]), post_data
        )

        self.assertEqual(response.status_code, 302)

        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Comment submitted and awaiting approval',
            response.content
        )

    def test_like_view_toggle(self):
        """
        Test toggling like/unlike functionality on a blog post.

        **Expectation**
        The user should be able to like and unlike the post, with the like status 
        being reflected in the post's 'likes' field.
        """
        self.client.login(username="testUsername", password="myPassword123")
        url = reverse('like_post', args=[self.post.pk])

        # Like the post
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())

        # Unlike the post
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.post.likes.filter(id=self.user.id).exists())

    def test_comment_edit_success(self):
        """
        Test editing an existing comment on a blog post.

        **Expectation**
        After submitting the form to edit the comment, the body of the comment 
        should be updated, and the comment should remain unapproved.
        """
        self.client.login(username="testUsername", password="myPassword123")
        edit_url = reverse('comment_edit', args=[self.post.slug, self.comment.pk])
        post_data = {'body': 'Updated test comment'}

        response = self.client.post(edit_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, 'Updated test comment')
        self.assertFalse(self.comment.approved)

    def test_comment_delete_success(self):
        """
        Test deleting a comment from a blog post.

        **Expectation**
        After submitting the form to delete the comment, the comment should 
        no longer exist in the database.
        """
        self.client.login(username="testUsername", password="myPassword123")
        delete_url = reverse('comment_delete', args=[self.post.slug, self.comment.pk])

        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_submit_blog_post(self):
        """
        Test submitting a new blog post.

        **Expectation**
        After submitting the form for a new blog post, the blog post should be 
        saved to the database, and the user should be redirected.
        """
        self.client.login(username="testUsername", password="myPassword123")
        url = reverse('submit_blog_post')
        post_data = {
            'title': 'New Test Blog Post',
            'description': 'This is a new blog post.',
            'intro ': 'A new blog post intro .'
        }

        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BlogPost.objects.filter(title="New Test Blog Post").exists())

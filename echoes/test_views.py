from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CommentForm
from .models import BlogPost


class TestBlogViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testUsername",
            password="myPassword123",
            email="test@test.com"
        )
        self.post = BlogPost(
            title="Echoes title",
            author=self.user,
            slug="echoes-title",
            excerpt="Echoes excerpt",
            content="Echoes content",
            status=1
        )
        self.post.save()

    def test_render_post_detail_page_with_comment_form(self):
        response = self.client.get(reverse('post_detail', args=['echoes-title']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Echoes title", response.content)
        self.assertIn(b"Echoes content", response.content)
        self.assertIsInstance(response.context['comment_form'], CommentForm)

    def test_successful_comment_submission(self):
        """Test for posting a comment on a post"""

        logged_in = self.client.login(
            username="testUsername", password="myPassword123"
        )
        self.assertTrue(logged_in)

        post_data = {
            'body': 'This is a test comment.'
        }

        response = self.client.post(
            reverse('post_detail', args=['echoes-title']), post_data
        )

        self.assertEqual(response.status_code, 302)

        response = self.client.get(response.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Comment submitted and awaiting approval',
            response.content
        )
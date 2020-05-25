from django.test import TestCase
from django.urls import reverse

from posts.models import User, Post


class TestPosts(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password=12345)
        self.text = 'test_text'

    def test_auth_user_post_creation(self):
        self.client.login(username=self.user.username,
                          password=12345)
        response = self.client.post(reverse('new_post'), {'text': self.text})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertContains(response, self.text)

    def test_anon_post_creation(self):
        # Test, if anon is able to retrieve the new_post page
        response = self.client.get(reverse('new_post'))
        self.assertRedirects(response=response,
                             expected_url='/auth/login?next=/new/',
                             target_status_code=301)

        # Test, if anon is able to create a post through a POST request.
        self.client.post(reverse('new_post'), {'text': self.text})
        post = Post.objects.filter(text=self.text).exists()
        self.assertFalse(post)

    def test_post_render_all(self):
        self.client.login(username=self.user.username, password=12345)
        post = Post.objects.create(text=self.text, author=self.user)

        # Profile test
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertContains(response, self.text)

        # Index page test
        response = self.client.get(reverse('index'))
        self.assertContains(response, self.text)

        # Test that there's only 1 post and it is ours
        posts_count = len(response.context['page'].object_list)
        self.assertEqual(posts_count, 1)
        post_text = str(response.context['page'].object_list[0])
        self.assertEqual(post_text, self.text)

        # Direct post's page test
        response = self.client.get(
            reverse('post_view',
                    kwargs={'username': 'testuser', 'post_id': post.pk}))
        self.assertContains(response, self.text)

    def test_edit_view(self):
        self.client.login(username=self.user.username, password=12345)
        post = Post.objects.create(text=self.text, author=self.user)
        post_count = Post.objects.all().count()

        # Check if the post's got created and renders properly
        response = self.client.get(reverse('index'))
        self.assertEqual(post_count, 1)
        self.assertContains(response, self.text)

        # Post editing
        text_edited = 'test_text_edit'
        self.client.post(reverse('post_edit',
                                 kwargs={'username': self.user.username,
                                         'post_id': post.pk}),
                         {'text': text_edited})

        # Test that no unwanted entities got created and contents are ok
        post_edited = Post.objects.get(pk=post.pk)
        post_count_edited = Post.objects.all().count()
        self.assertEqual(post, post_edited)
        self.assertEqual(post_edited.text, text_edited)
        self.assertEqual(post_count, post_count_edited)

        # Test connected pages and proper rendering
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertContains(response, text_edited)
        response = self.client.get(reverse('index'))
        self.assertContains(response, text_edited)
        response = self.client.get(reverse('post_view',
                                           kwargs={
                                               'username': self.user.username,
                                               'post_id': post_edited.pk})
                                   )
        self.assertContains(response, 'test_text_edit')

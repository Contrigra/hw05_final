from django.test import TestCase
from django.urls import reverse

from posts.models import User, Post


class TestPosts(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')

    def test_user_profile(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_data'].username,
                         self.user.username)

    def test_auth_user_post_creation(self):
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('new_post'), {'text': 'test_text'})
        response = self.client.get(
            reverse('profile', kwargs={'username': 'testuser'}))
        self.assertContains(response, 'test_text')

        self.assertContains(response, 'test_text')

    def test_anon_post_creation(self):
        response = self.client.get(reverse('new_post'))
        self.assertRedirects(response=response,
                             expected_url='/auth/login?next=/new/',
                             target_status_code=301)

    def test_post_render_all(self):
        self.client.login(username='testuser', password='12345')
        Post.objects.create(text='test_text', author=self.user)
        test_post_id = Post.objects.get(text='test_text').pk
        response = self.client.get('/testuser/')
        self.assertContains(response, 'test_text')
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'test_text')
        response = self.client.get(
            reverse('post',
                    kwargs={'username': 'testuser', 'post_id': test_post_id}))
        self.assertContains(response, 'test_text')

    def test_edit(self):
        self.client.login(username='testuser', password='12345')
        Post.objects.create(text='test_text', author=self.user)
        test_post_id = str(Post.objects.get(text='test_text').pk)
        # check if the post's got created
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'test_text')
        # post editing
        self.client.post(reverse('post_edit',
                                 kwargs={'username': 'testuser',
                                         'post_id': test_post_id}),
                         {'text': 'test_text_edit'})
        # check if the first post is the same entity as the second one
        edited_post_id = str(Post.objects.get(text='test_text_edit').pk)
        self.assertEqual(test_post_id, edited_post_id)
        # checking all connected pages
        response = self.client.get('/testuser/')
        self.assertContains(response, 'test_text_edit')
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'test_text_edit')
        response = self.client.get(reverse('post',
                                           kwargs={'username': 'testuser',
                                                   'post_id': test_post_id}))
        self.assertContains(response, 'test_text_edit')

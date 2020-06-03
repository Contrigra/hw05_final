from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from posts.models import User, Post, Group


class TestPostCreation(TestCase):
    """Test for proper post creation and protection from anons"""

    def setUp(self):
        self.text = 'test_text'
        self.user = User.objects.create_user(username='testuser',
                                             password=12345)

    def test_auth_user_post_creation(self):
        # Login into our user and check for redirection.
        self.client.login(username=self.user.username,
                          password=12345)
        response = self.client.post(reverse('new_post'), {'text': self.text})
        self.assertEqual(response.status_code, 302)

        # Test that the text is equal
        post = Post.objects.first()
        self.assertEqual(post.text, self.text)

    def test_anon_post_creation_redirect(self):
        # Test, if anon is able to retrieve the new_post page
        response = self.client.get(reverse('new_post'))
        self.assertRedirects(response=response,
                             expected_url='/auth/login?next=/new/',
                             target_status_code=301)

    def test_anon_post_creation_post_request(self):
        # Test, if anon is able to create a post through a POST request.
        self.client.post(reverse('new_post'), {'text': self.text})
        post_count = Post.objects.filter(text=self.text).count()
        self.assertEqual(post_count, 0)


class TestPostRender(TestCase):
    """Test for proper post's rendering."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password=12345)
        self.text = 'test_text'
        self.post = Post.objects.create(text=self.text, author=self.user)

    def test_profile(self):
        # Profile test
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertContains(response, self.text)

    def test_index(self):
        cache.clear()
        # Index page test
        response = self.client.get(reverse('index'))
        self.assertContains(response, self.text)

    def test_direct_post_view(self):
        # Direct post's page test
        response = self.client.get(
            reverse('post_view',
                    kwargs={'username': 'testuser', 'post_id': self.post.pk}))
        self.assertContains(response, self.text)


class TestPostEdit(TestCase):
    """Test for proper post editing."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password=12345)
        self.text = 'test_text'
        self.post = Post.objects.create(text=self.text, author=self.user)
        self.text_edited = 'test_text_edit'

    def test_post_edit(self):
        self.client.login(username=self.user.username, password=12345)

        # Post editing
        self.client.post(reverse('post_edit',
                                 kwargs={'username': self.user.username,
                                         'post_id': self.post.pk}),
                         {'text': self.text_edited})

        # Test that no unwanted entities got created and contents are ok
        post_edited = Post.objects.first()
        post_count = Post.objects.all().count()
        self.assertEqual(self.post, post_edited)
        self.assertEqual(post_edited.text, self.text_edited)
        self.assertEqual(post_count, 1)


@override_settings(CACHES={
    'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class TestEditedPostRender(TestCase):
    """Test for rendering edited posts."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password=12345)
        self.text = 'test_text'
        self.post = Post.objects.create(text=self.text, author=self.user)
        self.text_edited = 'test_text_edit'

    def test_post_render_all_pages(self):
        # Post editing
        self.client.login(username=self.user.username, password=12345)
        self.client.post(reverse('post_edit',
                                 kwargs={'username': self.user.username,
                                         'post_id': self.post.pk}),
                         {'text': self.text_edited})

        # Test for rendering
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertContains(response, self.text_edited)
        response = self.client.get(reverse('index'))
        self.assertContains(response, self.text_edited)
        response = self.client.get(reverse(
            'post_view',
            kwargs={
                'username': self.user.username,
                'post_id': Post.objects.first().pk})
        )
        self.assertContains(response, self.text_edited)


class TestHandlers(TestCase):
    """Test for custom error handlers"""

    def test_404(self):
        response = self.client.get('/test_non_existing_url_qweqwe/')
        self.assertEqual(response.status_code, 404)


class TestImageRender(TestCase):
    """Test for image handling,
    and rendering looking for <img tag in a response."""

    def setUp(self):
        self.tag = '<img'
        self.user = User.objects.create_user(username='testuser',
                                             password=12345)
        self.text = 'test_text'
        self.post = Post.objects.create(
            text=self.text, author=self.user,
            image='posts/test_image/Test_image.jpg'
        )

    def test_direct_post_image_render(self):
        response = self.client.get(
            reverse('post_view', kwargs={'username': self.user.username,
                                         'post_id': self.post.pk}))
        self.assertContains(response, self.tag)

    def test_profile_post_image_render(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertContains(response, self.tag)

    def test_group_post_Image_Render(self):
        # Creating a new group and assigning it to the existing test post
        self.group = Group.objects.create(title='Test group',
                                          slug='test-group',
                                          description='Test group description')
        self.post.group_id = self.group.pk
        self.post.save()

        response = self.client.get(
            reverse('group_posts', kwargs={'slug': self.group.slug}))
        self.assertContains(response, self.tag)


class TestImageFormProtection(TestCase):
    """Test for image form protection"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password=12345)
        self.client.force_login(self.user)
        self.post = Post.objects.create(text='test_text', author=self.user)
        self.image_path = 'media/posts/test_image/Test_image.jpg'
        self.non_image_path = 'posts/tests.py'
        self.error_message = f'Загрузите правильное изображение. Фа\
йл, который вы загрузили, поврежден или не является изображением.'

    def test_correct_image_form_protection(self):
        with open(self.image_path, 'rb') as img:
            self.client.post(reverse('post_edit',
                                     kwargs={
                                         'username': self.user.username,
                                         'post_id': self.post.pk}),
                             {'image': img,
                              'text': 'edited text with an image'})

            post = Post.objects.first()
            self.assertIsNotNone(post.image)

    def test_incorrect_image_form_protection(self):
        with open(self.non_image_path, 'rb') as non_img:
            response = self.client.post(reverse('post_edit',
                                                kwargs={
                                                    'username': self.user.username,
                                                    'post_id': self.post.pk}),
                                        {'image': non_img,
                                         'text': 'edited text with wrong file '})
            self.assertFormError(response, 'form', 'image', self.error_message)


class TestCache(TestCase):
    """Test for caching"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password=12345)
        self.client.force_login(self.user)
        self.text = 'test_text'

    def test_index_cache(self):
        # Create a cached page and check that there's no new post yet.
        self.client.get(reverse('index'))
        self.client.post(reverse('new_post'), {'text': self.text})
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, self.text)

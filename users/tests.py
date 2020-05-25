from django.test import TestCase
from django.urls import reverse


class TestUserProfile(TestCase):

    def test_user_profile_creation(self):
        # Test that there's no profile yet
        response = self.client.get(
            reverse('profile', kwargs={'username': 'test_profile'})
        )
        self.assertEqual(response.status_code, 404)
        # Create an user object and check for the profile page
        self.client.post(reverse('signup'),
                         {'username': 'test_profile',
                          'email': 'testmail@gmail.com',
                          'password1': 'password_test',
                          'password2': 'password_test'}
                         )
        response = self.client.get(
            reverse('profile', kwargs={'username': 'test_profile'}))
        self.assertEqual(response.status_code, 200)

from django.contrib.auth import get_user_model
from django.test import TestCase

class PetalUserTests(TestCase):

    def test_create_user(self):

        User = get_user_model()
        user = User.objects.create_user(
            username = "cku3",
            email = "cku3@zips.uakron.edu",
            password='testpass123'
        )
        self.assertEqual(user.username, "cku3")
        self.assertEqual(user.email, "cku3@zips.uakron.edu")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="oakinpel",
            email="olakunleakinpelu@gmail.com",
            password='Akindije@1'
        )
        self.assertEqual(admin_user.username, "oakinpel")
        self.assertEqual(admin_user.email, "olakunleakinpelu@gmail.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
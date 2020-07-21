from django.test import TestCase
from django.contrib.auth.models import User


class ProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test_username', password='test_password')
        user.profile.phone = '789787987'

    def test_phone_label(self):
        user = User.objects.get(username='test_username')
        field_label = user.profile._meta.get_field('phone').verbose_name
        self.assertEquals(field_label, 'phone')

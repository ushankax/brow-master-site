from django.contrib import auth
from django.urls import reverse
from django.test import TestCase

from booking.tests.test_views import ClientTestCase
from booking.models import Booking


class SignUpTests(TestCase):
    def test_signup_status_code(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class ProfileDetailTestView(ClientTestCase):

    def setUp(self):
        super().setUp()
        number_of_bookings = 8

        for booking_num in range(number_of_bookings):
            booking_num = Booking.objects.create(name='Name {}'.format(booking_num),
                                                 date='2020-0{}-22'.format(1 + booking_num),
                                                 time='17:00 - 19:00',
                                                 address='Мякинино',
                                                 work=Booking.WorkType.FIRST,
                                                 phone='456456456',
                                                 status='d'
                                                 )
            booking_num.client = self.super_user.profile
            booking_num.save()

    def test_login_user(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/profile/{}'.format(self.super_user.pk))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('user-profile', kwargs={'pk': self.super_user.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('user-profile', kwargs={'pk': self.super_user.pk}))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'user_profile.html')

    def test_pagination_is_five(self):
        resp = self.client.get(reverse('user-profile', kwargs={'pk': self.super_user.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('page_obj' in resp.context)
        self.assertEqual(len(resp.context['page_obj']), 5)

    def test_lists_all_authors(self):
        resp = self.client.get(reverse('user-profile', kwargs={'pk': self.super_user.pk}) + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('page_obj' in resp.context)
        self.assertTrue(len(resp.context['page_obj']) == 3)

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth

from booking.models import Booking


# Template for views when login required
class ClientTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.super_user = User.objects.create_superuser('supertest', password='superpassword')
        self.super_user.save()
        self.user = User.objects.create_user('test', password='password')
        self.user.save()
        self.login_superuser()

    def login_user(self):
        self.client.login(username='test', password='password')

    def login_superuser(self):
        self.client.login(username='supertest', password='superpassword')

    def test_login_user(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)


class IndexTestView(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'index.html')


class PricingTestView(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/pricing/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('pricing'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('pricing'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'pricing.html')


class ContactsTestView(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/contacts/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('contacts'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('contacts'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'contacts.html')


class BookingCreateTestView(ClientTestCase):

    def test_login_user(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/booking/create/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('booking-create'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('booking-create'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'booking/booking_form.html')

    def test_redirect_if_user_not_logged_in(self):
        self.client.logout()
        resp = self.client.get(reverse('booking-create'))
        self.assertRedirects(resp, '/accounts/login/?next=/booking/create/')

    def test_redirect_if_user_doesnt_have_permission(self):
        self.client.logout()
        self.login_user()

        resp = self.client.get(reverse('booking-create'))
        self.assertEqual(resp.status_code, 403)


class BookingListTestView(ClientTestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_bookings = 8

        for booking_num in range(number_of_bookings):
            Booking.objects.create(name='Name {}'.format(booking_num),
                                   date='2020-05-{}'.format(1 + booking_num),
                                   time='17:00 - 19:00',
                                   address='Мякинино',
                                   work=Booking.WorkType.FIRST,
                                   phone='456456456',
                                   )

    def test_login_user(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/booking/booking_list/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('bookings'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('bookings'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'booking_list.html')

    def test_pagination_is_five(self):
        resp = self.client.get(reverse('bookings'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('page_obj' in resp.context)
        self.assertTrue(len(resp.context['page_obj']) == 5)

    def test_lists_all_authors(self):
        resp = self.client.get(reverse('bookings') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('page_obj' in resp.context)
        self.assertTrue(len(resp.context['page_obj']) == 3)

    def test_redirect_if_user_not_logged_in(self):
        self.client.logout()
        resp = self.client.get(reverse('bookings'))
        self.assertRedirects(resp, '/accounts/login/?next=/booking/booking_list/')

    def test_redirect_if_user_doesnt_have_permission(self):
        self.client.logout()
        self.login_user()

        resp = self.client.get(reverse('bookings'))
        self.assertRedirects(resp, '/accounts/login/?next=/booking/booking_list/')


class DoneBookingListTestView(ClientTestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_bookings = 8

        for booking_num in range(number_of_bookings):
            Booking.objects.create(name='Name {}'.format(booking_num),
                                   date='2020-05-{}'.format(1 + booking_num),
                                   time='17:00 - 19:00',
                                   address='Мякинино',
                                   work=Booking.WorkType.FIRST,
                                   phone='456456456',
                                   status='d'
                                   )

    def test_login_user(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/booking/done_booking_list/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('bookings-done'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('bookings-done'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'done_booking_list.html')

    def test_pagination_is_five(self):
        resp = self.client.get(reverse('bookings-done'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('page_obj' in resp.context)
        self.assertTrue(len(resp.context['page_obj']) == 5)

    def test_lists_all_authors(self):
        resp = self.client.get(reverse('bookings-done') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('page_obj' in resp.context)
        self.assertTrue(len(resp.context['page_obj']) == 3)

    def test_redirect_if_user_not_logged_in(self):
        self.client.logout()
        resp = self.client.get(reverse('bookings-done'))
        self.assertRedirects(resp, '/accounts/login/?next=/booking/done_booking_list/')

    def test_redirect_if_user_doesnt_have_permission(self):
        self.client.logout()
        self.login_user()

        resp = self.client.get(reverse('bookings-done'))
        self.assertRedirects(resp, '/accounts/login/?next=/booking/done_booking_list/')


class BookingUpdateTestView(ClientTestCase):

    def setUp(self):
        super().setUp()
        self.booking = Booking.objects.create(name='Name',
                                              date='2020-05-05',
                                              time='17:00 - 19:00',
                                              address='Мякинино',
                                              work=Booking.WorkType.FIRST,
                                              phone='456456456',
                                              )

    def test_login_user(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/booking/{}/edit/'.format(self.booking.id))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('booking-edit', kwargs={'pk': self.booking.pk,}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('booking-edit', kwargs={'pk': self.booking.pk,}))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'booking/booking_form.html')

    def test_redirect_if_user_not_logged_in(self):
        self.client.logout()
        resp = self.client.get(reverse('booking-edit', kwargs={'pk': self.booking.pk,}))
        self.assertRedirects(resp, '/accounts/login/?next=/booking/{}/edit/'.format(self.booking.pk))

    def test_redirect_if_user_doesnt_have_permission(self):
        self.client.logout()
        self.login_user()

        resp = self.client.get(reverse('booking-edit', kwargs={'pk': self.booking.pk,}))
        self.assertEqual(resp.status_code, 403)


class BookingDeleteTestView(ClientTestCase):

    def setUp(self):
        super().setUp()
        self.booking = Booking.objects.create(name='Name',
                                              date='2020-05-05',
                                              time='17:00 - 19:00',
                                              address='Мякинино',
                                              work=Booking.WorkType.FIRST,
                                              phone='456456456',
                                              )

    def test_login_user(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/booking/{}/delete/'.format(self.booking.id))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('booking-delete', kwargs={'pk': self.booking.pk,}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('booking-delete', kwargs={'pk': self.booking.pk,}))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'booking/booking_confirm_delete.html')

    def test_redirect_if_user_not_logged_in(self):
        self.client.logout()
        resp = self.client.get(reverse('booking-delete', kwargs={'pk': self.booking.pk,}))
        self.assertRedirects(resp, '/accounts/login/?next=/booking/{}/delete/'.format(self.booking.pk))

    def test_redirect_if_user_doesnt_have_permission(self):
        self.client.logout()
        self.login_user()

        resp = self.client.get(reverse('booking-delete', kwargs={'pk': self.booking.pk,}))
        self.assertEqual(resp.status_code, 403)


class BonusRedirectTestView(ClientTestCase):

    def setUp(self):
        super().setUp()
        self.booking = Booking.objects.create(name='Name',
                                              date='2020-05-05',
                                              time='17:00 - 19:00',
                                              address='Мякинино',
                                              work=Booking.WorkType.FIRST,
                                              phone='456456456',
                                              )
        self.booking.client = self.super_user.profile
        self.booking.save()

    def test_login_user(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/booking/bonus/{}'.format(self.booking.pk))
        self.assertEqual(resp.status_code, 302)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('bonus', kwargs={'pk': self.booking.pk,}))
        self.assertEqual(resp.status_code, 302)

    def test_redirect_if_user_not_logged_in(self):
        self.client.logout()
        resp = self.client.get(reverse('bonus', kwargs={'pk': self.booking.pk, }))
        self.assertRedirects(resp, '/accounts/login/?next=/booking/bonus/{}'.format(self.booking.pk))

    def test_redirect_if_user_doesnt_have_permission(self):
        self.client.logout()
        self.login_user()

        resp = self.client.get(reverse('bonus', kwargs={'pk': self.booking.pk,}))
        self.assertEqual(resp.status_code, 403)

    def test_bonus_points_work(self):
        resp = self.client.get(reverse('bonus', kwargs={'pk': self.booking.pk,}))
        self.assertEqual(resp.status_code, 302)

        self.booking.refresh_from_db()
        self.super_user.refresh_from_db()

        self.assertEqual(self.booking.client.visits, 1)
        self.assertEqual(self.super_user.profile.visits, 1)
        self.assertEqual(self.super_user.profile.bonus_points, 150)
        self.assertEqual(self.booking.status, 'd')
        self.assertEqual(self.booking.price, 1500)

class BonusSpendTestView(ClientTestCase):

    def setUp(self):
        super().setUp()
        self.booking = Booking.objects.create(name='Name',
                                              date='2020-05-05',
                                              time='17:00 - 19:00',
                                              address='Мякинино',
                                              work=Booking.WorkType.FIRST,
                                              phone='456456456',
                                              )
        self.booking.client = self.super_user.profile
        self.booking.save()

    def test_login_user(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/booking/bonus/spend/{}'.format(self.booking.pk))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('bonus-spend', kwargs={'pk': self.booking.pk,}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('bonus-spend', kwargs={'pk': self.booking.pk,}))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'bonus_spend.html')

    def test_bonus_spend_works_correctly(self):
        resp = self.client.post(reverse('bonus-spend', kwargs={'pk': self.booking.pk,}), {'bonus_points': 50})

        self.booking.refresh_from_db()
        self.super_user.refresh_from_db()

        self.assertEqual(self.super_user.profile.visits, 1)
        self.assertEqual(self.booking.price, 1450)
        self.assertEqual(self.booking.status, 'd')

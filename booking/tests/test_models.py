from django.test import TestCase

from booking.models import Booking


class BookingModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Booking.objects.create(name='Sergey',
                               date='2020-10-12',
                               time='11:00 - 13:00',
                               address='Мякинино',
                               work=Booking.WorkType.FIRST,
                               phone='79014568989',
                               comment='test comment',
                               )

    def test_name_label(self):
        booking = Booking.objects.get(id=50)
        field_label = booking._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_date_label(self):
        booking = Booking.objects.get(id=50)
        field_label = booking._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'date')

    def test_time_label(self):
        booking = Booking.objects.get(id=50)
        field_label = booking._meta.get_field('time').verbose_name
        self.assertEquals(field_label, 'time')

    def test_address_label(self):
        booking = Booking.objects.get(id=50)
        field_label = booking._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')

    def test_work_label(self):
        booking = Booking.objects.get(id=50)
        field_label = booking._meta.get_field('work').verbose_name
        self.assertEquals(field_label, 'work')

    def test_phone_label(self):
        booking = Booking.objects.get(id=50)
        field_label = booking._meta.get_field('phone').verbose_name
        self.assertEquals(field_label, 'phone')

    def test_comment_label(self):
        booking = Booking.objects.get(id=50)
        field_label = booking._meta.get_field('comment').verbose_name
        self.assertEquals(field_label, 'comment')

    def test_str_view(self):
        booking = Booking.objects.get(id=50)
        expected_name = '{}, {}, {}'.format(booking.name, booking.date, booking.time)
        self.assertEquals(expected_name, str(booking))

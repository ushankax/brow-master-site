from django.test import TestCase

from booking.forms import BookingForm, BonusSpendForm
from booking.models import Booking


class BookingFormTest(TestCase):

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

    def test_booking_form_name_label(self):
        form = BookingForm()
        self.assertEquals(form.fields['name'].label, 'Имя')

    def test_booking_form_date_label(self):
        form = BookingForm()
        self.assertEquals(form.fields['date'].label, 'Дата')

    def test_booking_form_time_label(self):
        form = BookingForm()
        self.assertEquals(form.fields['time'].label, 'Время')

    def test_booking_form_address_label(self):
        form = BookingForm()
        self.assertEquals(form.fields['address'].label, 'Адрес')

    def test_booking_form_work_label(self):
        form = BookingForm()
        self.assertEquals(form.fields['work'].label, 'Услуга')

    def test_booking_form_phone_label(self):
        form = BookingForm()
        self.assertEquals(form.fields['phone'].label, 'Телефон')

    def test_booking_form_comment_label(self):
        form = BookingForm()
        self.assertEquals(form.fields['comment'].label, 'Комментарий')


class BonusSpendFormTest(TestCase):

    def test_bonus_spend_form_bonus_points_label(self):
        form = BonusSpendForm()
        self.assertEquals(form.fields['bonus_points'].label, 'Списать бонусов')
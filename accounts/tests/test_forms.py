from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.forms import SignUpForm


class SignUpFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='test_username', password='test_password')
        user1.profile.phone = '123456789'

    def test_signup_form_first_name_label(self):
        form = SignUpForm()
        self.assertEquals(form.fields['first_name'].label, 'Имя')

    def test_signup_form_username_label(self):
        form = SignUpForm()
        self.assertEquals(form.fields['username'].label, 'Имя пользователя')

    def test_signup_form_phone_label(self):
        form = SignUpForm()
        self.assertEquals(form.fields['phone'].label, 'Телефон')

    def test_signup_form_email_label(self):
        form = SignUpForm()
        self.assertEquals(form.fields['email'].label, 'Эл. почта')

    def test_signup_form_password_label(self):
        form = SignUpForm()
        self.assertEquals(form.fields['password1'].label, 'Пароль')

    def test_signup_form_password_repeat_label(self):
        form = SignUpForm()
        self.assertEquals(form.fields['password2'].label, 'Подтверждение пароля')

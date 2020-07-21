from django.test import TestCase

from booking.telegram import telegram_bot_sendtext


class TelegramMessageTest(TestCase):

    def test_send_message(self):
        text = 'you got it'
        self.assertEqual(telegram_bot_sendtext(text)['ok'], True)
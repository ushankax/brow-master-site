import logging

from pandabrow.celery import app


@app.task
def telegram_bot_sendtext_task(text):
    from booking.telegram import telegram_bot_sendtext

    telegram_bot_sendtext(text)
from django.db import models

from accounts.models import Profile


class Booking(models.Model):

    AVAILABLE_TIME = (
        ('1', '11:00 - 13:00'),
        ('2', '13:00 - 15:00'),
        ('3', '15:00 - 17:00'),
        ('4', '17:00 - 19:00'),
    )

    AVAILABLE_ADDRESSES = (
        ('m', 'Мякинино'),
        ('c', 'Чеховская'),
    )

    BOOKING_STATUS = (
        ('p', 'Process'),
        ('d', 'Done')
    )

    class WorkType(models.TextChoices):
        FIRST = '1', 'Ламинирование'
        SECOND = '2', 'Ламинирование + коррекция'
        THIRD = '3', 'Ламинирование + окрашивание'
        FOURTH = '4', 'Ламинирование + коррекция + окрашивание'
        FIFTH = '5', 'Протеиновое восстановление'
        SIXTH = '6', 'Коррекция бровей пинцетом'
        SEVENTH = '7', 'Окрашивание бровей'
        EIGHTH = '8', 'Архитектура + окрашивание'
        NINETH = '9', 'Эпиляция над губой'
        TENTH = '10', 'Осветление'
        ELEVENTH = '11', 'Осветление + коррекция'

    PRICE_LIST = {
        '1': '1500',
        '2': '1700',
        '3': '1700',
        '4': '1900',
        '5': '1700',
        '6': '500',
        '7': '500',
        '8': '800',
        '9': '250',
        '10': '500',
        '11': '800',
    }

    client = models.ForeignKey(Profile,
                               related_name='bookings',
                               on_delete=models.SET_NULL,
                               null=True, blank=True)
    name = models.CharField(max_length=255)
    date = models.DateField(max_length=255, null=True)
    time = models.CharField(max_length=255, choices=AVAILABLE_TIME)
    address = models.CharField(max_length=255, choices=AVAILABLE_ADDRESSES)
    work = models.CharField(max_length=255, choices=WorkType.choices)
    phone = models.CharField(max_length=255)
    comment = models.TextField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=BOOKING_STATUS, default='p')
    price = models.IntegerField(default=0, null=True)
    booking_bonus = models.IntegerField(default=0)
    bonus_spent = models.IntegerField(default=0)

    def __str__(self):
        return '{}, {}, {}'.format(self.name, self.date, self.time)

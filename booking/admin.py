from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'address', 'work', 'phone', 'status')
    list_filter = ('date', 'address', 'status')

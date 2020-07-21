from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookingView.as_view(), name='booking'),
    path('<int:pk>/delete/', views.BookingDelete.as_view(), name='booking-delete'),
    path('<int:pk>/edit/', views.BookingUpdate.as_view(), name='booking-edit'),
    path('create/', views.BookingCreate.as_view(), name='booking-create'),
    path('booking_list/', views.booking_list, name='bookings'),
    path('done_booking_list/', views.done_booking_list, name='bookings-done'),
    path('bonus/<int:pk>', views.BonusRedirectView.as_view(), name='bonus'),
    path('bonus/spend/<int:pk>', views.BonusSpendView.as_view(), name='bonus-spend')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib import admin
from django.urls import path, include

from accounts import views as accounts_views
from booking import views as booking_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include('booking.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', accounts_views.SignUpView.as_view(), name='signup'),
    path('profile/', include('accounts.urls')),
    path('', booking_views.IndexView.as_view(), name='index'),
    path('pricing/', booking_views.PricingView.as_view(), name='pricing'),
    path('contacts/', booking_views.ContactsView.as_view(), name='contacts'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.ProfileDetailView.as_view(), name='user-profile'),
    path('<int:pk>/update', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('edit/', views.UpdateProfileView.as_view(), name='profile-edit')
]
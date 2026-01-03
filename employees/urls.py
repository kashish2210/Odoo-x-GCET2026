from django.urls import path
from employees import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/update-avatar/', views.update_profile_avatar, name='update_profile_avatar'),
]
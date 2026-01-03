from django.urls import path
from employees import views

app_name = 'employee'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('', views.employees, name='employees'),
    path('profile/update-avatar/', views.update_profile_avatar, name='update_profile_avatar'),
]
from django.urls import path
from employees import views

app_name = 'employee'

urlpatterns = [
    # Employee list (card view)
    path('', views.employees, name='employees'),
    
    # Add employee
    path('add/', views.add_employee, name='add_employee'),
    
    # Individual employee detail (view-only)
    path('<int:employee_id>/', views.employee_detail, name='employee_detail'),
    
    # Current user's profile
    path('profile/', views.profile, name='profile'),
    
    # Update avatar
    path('profile/update-avatar/', views.update_profile_avatar, name='update_profile_avatar'),
]
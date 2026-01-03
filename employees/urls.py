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
    
    # Update endpoints
    path('profile/update-avatar/', views.update_profile_avatar, name='update_profile_avatar'),
    path('profile/update-employee-profile/', views.update_employee_profile, name='update_employee_profile'),
    path('profile/update-private-info/', views.update_private_info, name='update_private_info'),
    path('profile/update-salary-info/', views.update_salary_info, name='update_salary_info'),
    path('profile/upload-resume/', views.upload_resume, name='upload_resume'),
]
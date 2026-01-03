from django.urls import path
from . import views

app_name = 'timeoff'

urlpatterns = [
    # List view
    path('', views.timeoff_list, name='timeoff_list'),
    
    # Request time off
    path('request/', views.request_timeoff, name='request_timeoff'),
    
    # Approve/Reject (Admin/Manager only)
    path('approve/<int:request_id>/', views.approve_timeoff, name='approve_timeoff'),
    path('reject/<int:request_id>/', views.reject_timeoff, name='reject_timeoff'),
    
    # Detail view
    path('<int:request_id>/', views.timeoff_detail, name='timeoff_detail'),
]
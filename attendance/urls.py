from django.urls import path
from .views import attendance, check_in_out_view, attendance_list_view

app_name = "attendance"

urlpatterns = [
    path('', attendance, name='attendance'),
    path('toggle/', check_in_out_view, name='toggle'),
    path('list/', attendance_list_view, name='list')
]
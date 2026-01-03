from django.urls import path
from .views import attendance

app_name = "attendance"

urlpatterns = [
    path('', attendance, name='attendance')
]
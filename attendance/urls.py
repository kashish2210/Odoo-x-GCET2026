from django.urls import path
from .views import attendance

urlpatterns = [
    path('', attendance)
]
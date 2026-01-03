from django.contrib import admin
from .models import PrivateInfo, EmployeeProfile

# Register your models here.
admin.site.register([PrivateInfo, EmployeeProfile])
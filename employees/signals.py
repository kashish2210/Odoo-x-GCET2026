from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EmployeeProfile, PrivateInfo, SalaryInfo, ProvidentFund


User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_employee_profile_and_private_info(sender, instance, created, **kwargs):
    if not created:
        return

    profile = EmployeeProfile.objects.create(
        user=instance,
        job_position="",
        phone="",
        company="",
        department="",
        location=""
    )

    PrivateInfo.objects.create(profile=profile)

    salary_info = SalaryInfo.objects.create(profile=profile)

    ProvidentFund.objects.create(salary_info=salary_info)
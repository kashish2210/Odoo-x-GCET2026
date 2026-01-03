from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    job_position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    company = models.CharField(max_length=150)
    department = models.CharField(max_length=100)

    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_employees",
        help_text="Reporting manager"
    )

    location = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.job_position}"


class PrivateInfo(models.Model):
    profile = models.OneToOneField(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name="private_info"
    )

    # Personal Details
    date_of_birth = models.DateField(null=True, blank=True)
    residing_address = models.TextField(blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    personal_email = models.EmailField(blank=True)

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True
    )

    MARITAL_STATUS_CHOICES = [
        ("SINGLE", "Single"),
        ("MARRIED", "Married"),
        ("DIVORCED", "Divorced"),
    ]
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        blank=True
    )

    date_of_joining = models.DateField(null=True, blank=True)

    # Bank Details
    account_number = models.CharField(max_length=30, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)

    pan_no = models.CharField(max_length=20, blank=True)
    uan_no = models.CharField(max_length=30, blank=True)
    emp_code = models.CharField(max_length=30, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Private Info - {self.profile.user}"

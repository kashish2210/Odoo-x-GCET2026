from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, login_id, email, password=None, **extra_fields):
        if not login_id:
            raise ValueError("Employee ID / Login ID is required")
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        
        user = self.model(
            login_id=login_id,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, login_id, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)
        return self.create_user(login_id, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        EMPLOYEE = "EMPLOYEE", "Employee"
        HR = "HR", "HR"
        ADMIN = "ADMIN", "Admin"
    
    login_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="Employee ID / Login ID"
    )
    email = models.EmailField(unique=True)
    
    # Company Logo
    company_logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True,
        help_text="Company logo"
    )
    
    # Profile Avatar
    profile_avatar = models.ImageField(
        upload_to='profile_avatars/',
        blank=True,
        null=True,
        help_text="User profile picture"
    )
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.HR
    )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Check-in status
    is_checked_in = models.BooleanField(default=False)
    done_for_day = models.BooleanField(null=True, blank=True )
    last_check_in = models.DateTimeField(null=True, blank=True)
    last_check_out = models.DateTimeField(null=True, blank=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = "login_id"
    REQUIRED_FIELDS = ["email"]
    
    def __str__(self):
        return f"{self.login_id} ({self.email})"
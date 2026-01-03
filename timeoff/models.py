from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL


class TimeOffType(models.Model):
    """Types of time off (Paid Time Off, Sick Leave, Unpaid Leave)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class TimeOffRequest(models.Model):
    """Employee time off requests"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='timeoff_requests'
    )
    
    time_off_type = models.ForeignKey(
        TimeOffType,
        on_delete=models.PROTECT,
        related_name='requests'
    )
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Allocation/duration in days
    allocation = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Number of days requested"
    )
    
    validity_period_start = models.DateField(
        help_text="Start of validity period (e.g., May 13)"
    )
    validity_period_end = models.DateField(
        help_text="End of validity period (e.g., May 14)"
    )
    
    reason = models.TextField(blank=True)
    
    # Attachment for sick leave certificates
    attachment = models.FileField(
        upload_to='timeoff_attachments/',
        blank=True,
        null=True,
        help_text="For sick leave certificates"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Approval tracking
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_timeoff_requests'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.login_id} - {self.time_off_type.name} ({self.start_date} to {self.end_date})"
    
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date must be after start date")
        
        if self.validity_period_end < self.validity_period_start:
            raise ValidationError("Validity period end must be after start")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def days_available(self):
        """Calculate available days based on validity period"""
        # This is a simplified calculation
        # You may want to implement more complex logic based on your business rules
        return 26  # Default value shown in your design
    
    @property
    def days_remaining(self):
        """Calculate remaining days after this request"""
        return self.days_available - float(self.allocation)


class TimeOffBalance(models.Model):
    """Track employee time off balances"""
    
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='timeoff_balances'
    )
    
    time_off_type = models.ForeignKey(
        TimeOffType,
        on_delete=models.CASCADE,
        related_name='balances'
    )
    
    total_days = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=26.00,
        help_text="Total days allocated per year"
    )
    
    used_days = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00
    )
    
    year = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['employee', 'time_off_type', 'year']
        ordering = ['-year']
    
    def __str__(self):
        return f"{self.employee.login_id} - {self.time_off_type.name} ({self.year})"
    
    @property
    def available_days(self):
        return self.total_days - self.used_days
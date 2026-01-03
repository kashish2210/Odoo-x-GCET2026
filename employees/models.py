from django.conf import settings
from django.db import models
from decimal import Decimal

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
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
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
    date_of_birth = models.DateField(null=True, blank=True)
    residing_address = models.TextField(blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    personal_email = models.EmailField(blank=True)

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    MARITAL_STATUS_CHOICES = [
        ("SINGLE", "Single"),
        ("MARRIED", "Married"),
        ("DIVORCED", "Divorced"),
    ]
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
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


class SalaryInfo(models.Model):
    profile = models.OneToOneField(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name="salary_info"
    )
    monthly_wage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    yearly_wage = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    working_days_per_week = models.PositiveSmallIntegerField(default=5)
    break_time_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-calculate yearly wage
        if self.monthly_wage:
            self.yearly_wage = self.monthly_wage * 12
        super().save(*args, **kwargs)

    def calculate_components(self):
        """Calculate all salary components based on monthly wage"""
        if not self.monthly_wage:
            return
        
        wage = Decimal(str(self.monthly_wage))
        
        # Delete existing components
        self.components.all().delete()
        
        # Basic - 50% of wage
        basic = wage * Decimal('0.50')
        SalaryComponent.objects.create(
            salary_info=self,
            component_type='Basic',
            monthly_amount=basic,
            percentage_of_basic=Decimal('50.00')
        )
        
        # HRA - 50% of Basic
        hra = basic * Decimal('0.50')
        SalaryComponent.objects.create(
            salary_info=self,
            component_type='House Rent Allowance',
            monthly_amount=hra,
            percentage_of_basic=Decimal('50.00')
        )
        
        # Standard Allowance - Fixed 4167
        standard = Decimal('4167.00')
        SalaryComponent.objects.create(
            salary_info=self,
            component_type='Standard Allowance',
            monthly_amount=standard,
            percentage_of_basic=None
        )
        
        # Performance Bonus - 8.33% of Basic
        performance = basic * Decimal('0.0833')
        SalaryComponent.objects.create(
            salary_info=self,
            component_type='Performance Bonus',
            monthly_amount=performance,
            percentage_of_basic=Decimal('8.33')
        )
        
        # Leave Travel Allowance - 8.333% of Basic
        lta = basic * Decimal('0.08333')
        SalaryComponent.objects.create(
            salary_info=self,
            component_type='Leave Travel Allowance',
            monthly_amount=lta,
            percentage_of_basic=Decimal('8.33')
        )
        
        # Fixed Allowance - Remaining amount
        total_components = basic + hra + standard + performance + lta
        fixed = wage - total_components
        SalaryComponent.objects.create(
            salary_info=self,
            component_type='Fixed Allowance',
            monthly_amount=fixed,
            percentage_of_basic=None
        )
        
        # Create/Update PF
        pf, created = ProvidentFund.objects.get_or_create(salary_info=self)
        pf.employee_contribution = basic * Decimal('0.12')
        pf.employer_contribution = basic * Decimal('0.12')
        pf.save()
        
        # Create/Update Professional Tax
        tax, created = TaxDeduction.objects.get_or_create(
            salary_info=self,
            deduction_type='Professional Tax',
            defaults={'monthly_amount': Decimal('200.00')}
        )
        if not created:
            tax.monthly_amount = Decimal('200.00')
            tax.save()

    def __str__(self):
        return f"Salary Info - {self.profile.user}"


class ProvidentFund(models.Model):
    salary_info = models.OneToOneField(
        SalaryInfo,
        on_delete=models.CASCADE,
        related_name="pf"
    )
    employee_contribution = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    employee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)
    employer_contribution = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    employer_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)
    calculated_on_basic = models.BooleanField(default=True)

    def __str__(self):
        return f"PF - {self.salary_info.profile.user}"


class TaxDeduction(models.Model):
    salary_info = models.ForeignKey(
        SalaryInfo,
        on_delete=models.CASCADE,
        related_name="tax_deductions"
    )
    deduction_type = models.CharField(max_length=50)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.deduction_type} - {self.salary_info.profile.user}"


class SalaryComponent(models.Model):
    salary_info = models.ForeignKey(
        SalaryInfo,
        on_delete=models.CASCADE,
        related_name="components"
    )
    component_type = models.CharField(max_length=50)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage_of_basic = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.component_type} - {self.salary_info.profile.user}"
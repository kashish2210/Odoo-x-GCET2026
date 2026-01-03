from django import forms
from django.contrib.auth import get_user_model
from .models import EmployeeProfile, PrivateInfo, SalaryInfo, SalaryComponent, ProvidentFund, TaxDeduction

User = get_user_model()


class AddEmployeeForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=[('', 'Select Role')] + list(User._meta.get_field('role').choices),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    
    class Meta:
        model = User
        fields = ['login_id', 'email', 'role', 'profile_avatar']
        widgets = {
            'login_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter employee login ID'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'employee@company.com'
            }),
            'profile_avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_avatar']
        widgets = {
            'profile_avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'profileAvatarInput'
            })
        }


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['job_position', 'phone', 'company', 'department', 'manager', 'location']
        widgets = {
            'job_position': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PrivateInfoForm(forms.ModelForm):
    class Meta:
        model = PrivateInfo
        fields = [
            'date_of_birth', 'residing_address', 'nationality', 'personal_email',
            'gender', 'marital_status', 'date_of_joining', 'account_number',
            'bank_name', 'ifsc_code', 'pan_no', 'uan_no', 'emp_code'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'residing_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'personal_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control'}),
            'pan_no': forms.TextInput(attrs={'class': 'form-control'}),
            'uan_no': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_code': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SalaryInfoForm(forms.ModelForm):
    class Meta:
        model = SalaryInfo
        fields = ['monthly_wage', 'yearly_wage', 'working_days_per_week', 'break_time_hours']
        widgets = {
            'monthly_wage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'yearly_wage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
            'working_days_per_week': forms.NumberInput(attrs={'class': 'form-control'}),
            'break_time_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class ResumeUploadForm(forms.ModelForm):
    resume = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx'
        })
    )
    
    class Meta:
        model = EmployeeProfile
        fields = []
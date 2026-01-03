from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class AddEmployeeForm(forms.ModelForm):
    # Get the role choices from the User model
    role = forms.ChoiceField(
        choices=[('', 'Select Role')] + list(User._meta.get_field('role').choices),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    
    class Meta:
        model = User
        fields = [
            'login_id',
            'email',
            'role',
            'profile_avatar',
        ]
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


class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'role',
            'profile_avatar',
        ]


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
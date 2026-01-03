from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'login_id',
            'email',
            'role',
            'profile_avatar',
        ]


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

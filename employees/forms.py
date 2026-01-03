from django import forms
from django.conf import settings

User = settings.AUTH_USER_MODEL


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
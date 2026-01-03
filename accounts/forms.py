from allauth.account.forms import SignupForm
from django import forms
from .models import User


class CustomSignupForm(SignupForm):
    login_id = forms.CharField(
        max_length=50,
        label="Employee ID",
        widget=forms.TextInput(attrs={
            'placeholder': 'Employee ID',
            'class': 'form-control',
            'id': 'id_login_id'
        })
    )
    
    company_logo = forms.ImageField(
        required=False,
        label="Company Logo",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'id_logo',
            'accept': 'image/*'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email Address',
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-control'
        })

    def clean_login_id(self):
        login_id = self.cleaned_data.get('login_id')
        if User.objects.filter(login_id=login_id).exists():
            raise forms.ValidationError('This Employee ID is already taken. Please use a different one.')
        return login_id

    def save(self, request):
        user = super().save(request)
        user.login_id = self.cleaned_data["login_id"]
        
        # Save company logo
        if self.cleaned_data.get("company_logo"):
            user.company_logo = self.cleaned_data["company_logo"]
        
        user.save()
        return user
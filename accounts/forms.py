from allauth.account.forms import SignupForm
from django import forms


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
    
    company_name = forms.CharField(
        max_length=100,
        label="Company Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'Company Name',
            'class': 'form-control',
            'id': 'id_company_name'
        })
    )
    
    phone = forms.CharField(
        max_length=15,
        label="Phone",
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone Number',
            'class': 'form-control',
            'type': 'tel',
            'id': 'id_phone'
        })
    )
    
    logo = forms.ImageField(
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
        # Add styling to default allauth fields
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

    def save(self, request):
        user = super().save(request)
        user.login_id = self.cleaned_data["login_id"]
        # Save additional fields to user model or related profile model
        # user.company_name = self.cleaned_data.get("company_name")
        # user.phone = self.cleaned_data.get("phone")
        # Handle logo upload if you have a profile model
        # if self.cleaned_data.get("logo"):
        #     user.profile.logo = self.cleaned_data["logo"]
        #     user.profile.save()
        user.save()
        return user
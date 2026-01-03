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
        user.save()
        return user
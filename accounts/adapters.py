from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.forms import LoginForm
from django import forms


class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom adapter to modify allauth forms"""
    
    def get_login_form_class(self):
        """Return custom login form with styling"""
        class CustomLoginForm(LoginForm):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # Add styling to login form fields
                self.fields['login'].widget.attrs.update({
                    'placeholder': '',
                    'class': 'form-control'
                })
                self.fields['password'].widget.attrs.update({
                    'placeholder': '',
                    'class': 'form-control'
                })
        
        return CustomLoginForm
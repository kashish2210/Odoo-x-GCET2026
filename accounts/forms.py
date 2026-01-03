from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    login_id = forms.CharField(
        max_length=50,
        label="Employee ID"
    )

    def save(self, request):
        user = super().save(request)
        user.login_id = self.cleaned_data["login_id"]
        user.save()
        return user

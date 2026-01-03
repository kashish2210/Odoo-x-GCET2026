from django import forms
from .models import TimeOffRequest, TimeOffType


class TimeOffRequestForm(forms.ModelForm):
    class Meta:
        model = TimeOffRequest
        fields = [
            'time_off_type',
            'start_date',
            'end_date',
            'allocation',
            'validity_period_start',
            'validity_period_end',
            'reason',
            'attachment',
        ]
        widgets = {
            'time_off_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'allocation': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': '0.5',
                'placeholder': '01.00',
                'required': True
            }),
            'validity_period_start': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'validity_period_end': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter reason for time off...'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.png,.jpg,.jpeg'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        validity_start = cleaned_data.get('validity_period_start')
        validity_end = cleaned_data.get('validity_period_end')
        
        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date must be after start date")
        
        if validity_start and validity_end:
            if validity_end < validity_start:
                raise forms.ValidationError("Validity period end must be after start")
        
        return cleaned_data
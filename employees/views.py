from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import EmployeeProfile

@login_required()
def profile(request):
    profile = EmployeeProfile.objects.get(user = request.user.id)
    salary_info = getattr(profile, 'salary_info', None)

    context = {
        "salary_info": salary_info,
        "components": salary_info.components.all() if salary_info else [],
        "pf": getattr(salary_info, 'pf', None),
        "tax_deductions": salary_info.tax_deductions.all() if salary_info else []
    }

    return render(request, 'employees/profile.html', context=context)

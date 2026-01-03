from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import EmployeeProfile


@login_required
def profile(request):
    # Get or create employee profile
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)
    
    # Get salary info if exists
    salary_info = getattr(profile, 'salary_info', None)

    context = {
        "salary_info": salary_info,
        "components": salary_info.components.all() if salary_info else [],
        "pf": getattr(salary_info, 'pf', None),
        "tax_deductions": salary_info.tax_deductions.all() if salary_info else []
    }

    return render(request, 'employees/profile.html', context=context)


@login_required
def update_profile_avatar(request):
    """Handle profile avatar upload via AJAX"""
    if request.method == 'POST' and request.FILES.get('profile_avatar'):
        try:
            request.user.profile_avatar = request.FILES['profile_avatar']
            request.user.save()
            messages.success(request, 'Profile picture updated successfully!')
            return JsonResponse({
                'success': True, 
                'avatar_url': request.user.profile_avatar.url
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'No file uploaded'})
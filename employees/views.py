from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import date
from .models import EmployeeProfile, PrivateInfo, SalaryInfo
from .forms import (
    AddEmployeeForm, ProfileAvatarForm, EmployeeProfileForm,
    PrivateInfoForm, SalaryInfoForm, ResumeUploadForm
)

User = get_user_model()


def get_employee_attendance_status(employee):
    today = date.today()
    try:
        from attendance.models import Attendance
        attendance = Attendance.objects.filter(user=employee, date=today).first()
        if attendance and attendance.check_in:
            return 'present'
    except (ImportError, Exception):
        pass
    
    try:
        from leave.models import LeaveRequest
        leave = LeaveRequest.objects.filter(
            user=employee,
            start_date__lte=today,
            end_date__gte=today,
            status='approved'
        ).first()
        if leave:
            return 'on_leave'
    except (ImportError, Exception):
        pass
    
    return 'absent'


@login_required
def employees(request):
    employees_list = User.objects.all()
    for employee in employees_list:
        employee.attendance_status = get_employee_attendance_status(employee)
    
    context = {'employees': employees_list}
    return render(request, 'employees/employees.html', context)


@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(User, id=employee_id)
    
    try:
        profile = employee.profile
    except:
        profile = None
    
    try:
        private_info = profile.private_info if profile else None
    except:
        private_info = None
    
    try:
        salary_info = profile.salary_info if profile else None
    except:
        salary_info = None
    
    context = {
        'employee': employee,
        'profile': profile,
        'private_info': private_info,
        'salary_info': salary_info,
    }
    return render(request, 'employees/employee_detail.html', context)


@login_required
def profile(request):
    user = request.user
    
    try:
        profile = user.profile
    except:
        profile, _ = EmployeeProfile.objects.get_or_create(
            user=user,
            defaults={
                'job_position': 'Not specified',
                'phone': '',
                'company': '',
                'department': '',
                'location': ''
            }
        )
    
    try:
        private_info = profile.private_info
    except:
        private_info = None
    
    try:
        salary_info = profile.salary_info
        components = salary_info.components.all() if salary_info else []
        pf = salary_info.pf if salary_info else None
        tax_deductions = salary_info.tax_deductions.all() if salary_info else []
    except:
        salary_info = None
        components = []
        pf = None
        tax_deductions = []
    
    context = {
        'user': user,
        'profile': profile,
        'private_info': private_info,
        'salary_info': salary_info,
        'components': components,
        'pf': pf,
        'tax_deductions': tax_deductions,
    }
    return render(request, 'employees/profile.html', context)


@login_required
@require_http_methods(["POST"])
def update_profile_avatar(request):
    """Update user's profile avatar - returns JSON response"""
    try:
        if 'profile_avatar' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No file uploaded'
            }, status=400)
        
        user = request.user
        avatar_file = request.FILES['profile_avatar']
        
        # Validate file type
        if not avatar_file.content_type.startswith('image/'):
            return JsonResponse({
                'success': False,
                'error': 'Please upload an image file'
            }, status=400)
        
        # Validate file size (5MB max)
        if avatar_file.size > 5 * 1024 * 1024:
            return JsonResponse({
                'success': False,
                'error': 'Image size must be less than 5MB'
            }, status=400)
        
        # Update avatar
        user.profile_avatar = avatar_file
        user.save()
        
        return JsonResponse({
            'success': True,
            'avatar_url': user.profile_avatar.url if user.profile_avatar else None,
            'message': 'Profile picture updated successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def update_employee_profile(request):
    try:
        profile = request.user.profile
    except:
        profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)
    
    form = EmployeeProfileForm(request.POST, instance=profile)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully!')
    else:
        messages.error(request, 'Error updating profile.')
    
    return redirect('employee:profile')


@login_required
@require_http_methods(["POST"])
def update_private_info(request):
    try:
        profile = request.user.profile
    except:
        profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)
    
    try:
        private_info = profile.private_info
    except:
        private_info = PrivateInfo.objects.create(profile=profile)
    
    form = PrivateInfoForm(request.POST, instance=private_info)
    if form.is_valid():
        form.save()
        messages.success(request, 'Private information updated successfully!')
    else:
        messages.error(request, 'Error updating private information.')
    
    return redirect('employee:profile')


@login_required
@require_http_methods(["POST"])
def update_salary_info(request):
    # Check if user is admin
    if request.user.role != 'admin':
        messages.error(request, 'Only admins can update salary information.')
        return redirect('employee:profile')
    
    try:
        profile = request.user.profile
    except:
        profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)
    
    try:
        salary_info = profile.salary_info
    except:
        salary_info = SalaryInfo.objects.create(profile=profile)
    
    form = SalaryInfoForm(request.POST, instance=salary_info)
    if form.is_valid():
        salary_info = form.save()
        # Auto-calculate all components
        salary_info.calculate_components()
        messages.success(request, 'Salary information updated successfully!')
    else:
        messages.error(request, 'Error updating salary information.')
    
    return redirect('employee:profile')


@login_required
@require_http_methods(["POST"])
def upload_resume(request):
    try:
        profile = request.user.profile
    except:
        profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)
    
    if 'resume' in request.FILES:
        profile.resume = request.FILES['resume']
        profile.save()
        messages.success(request, 'Resume uploaded successfully!')
    else:
        messages.error(request, 'No file selected.')
    
    return redirect('employee:profile')


@login_required
def add_employee(request):
    from .forms import AddEmployeeForm
    from .models import EmployeeProfile
    
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST, request.FILES)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'employees/add_employee.html', {'form': form})
        
        if password and len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return render(request, 'employees/add_employee.html', {'form': form})
        
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(password)
                user.save()
                
                profile, created = EmployeeProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'job_position': 'Not specified',
                        'phone': '',
                        'company': '',
                        'department': '',
                        'location': ''
                    }
                )
                
                messages.success(request, f'Employee {user.login_id} added successfully!')
                return redirect('employee:employees')
            except Exception as e:
                messages.error(request, f'Error creating employee: {str(e)}')
                if 'user' in locals():
                    try:
                        user.delete()
                    except:
                        pass
                return render(request, 'employees/add_employee.html', {'form': form})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return render(request, 'employees/add_employee.html', {'form': form})
    else:
        form = AddEmployeeForm()
    
    return render(request, 'employees/add_employee.html', {'form': form})
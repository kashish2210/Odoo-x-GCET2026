from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date

User = get_user_model()


def get_employee_attendance_status(employee):
    """
    Determine the attendance status of an employee.
    Returns: 'present', 'on_leave', or 'absent'
    """
    today = date.today()
    
    # Check if employee has checked in today
    try:
        from attendance.models import Attendance  # Adjust import based on your app structure
        
        # If check_in is a TimeField and date is a DateField
        attendance = Attendance.objects.filter(
            user=employee,
            date=today  # Assuming there's a 'date' field
        ).first()
        
        if attendance and attendance.check_in:
            return 'present'
    except (ImportError, Exception):
        pass
    
    # Check if employee is on leave today
    try:
        from leave.models import LeaveRequest  # Adjust import based on your app structure
        
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
    
    # If no attendance and no leave, employee is absent
    return 'absent'


@login_required
def employees(request):
    """Display all employees in card view with attendance status"""
    # Get all users, don't require profile to exist
    employees_list = User.objects.all()
    
    # Add attendance status to each employee
    for employee in employees_list:
        employee.attendance_status = get_employee_attendance_status(employee)
    
    context = {
        'employees': employees_list
    }
    return render(request, 'employees/employees.html', context)


@login_required
def employee_detail(request, employee_id):
    """Display individual employee profile (view-only mode)"""
    employee = get_object_or_404(User, id=employee_id)
    
    # Get related profile information
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
    """Display logged-in user's own profile"""
    user = request.user
    
    try:
        profile = user.profile
    except:
        profile = None
    
    try:
        private_info = profile.private_info if profile else None
    except:
        private_info = None
    
    context = {
        'user': user,
        'profile': profile,
        'private_info': private_info,
    }
    return render(request, 'employees/profile.html', context)


@login_required
def update_profile_avatar(request):
    """Update user's profile avatar"""
    if request.method == 'POST':
        from .forms import ProfileAvatarForm
        
        form = ProfileAvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('employee:profile')
    
    return redirect('employee:profile')


@login_required
def add_employee(request):
    """Add a new employee"""
    from .forms import AddEmployeeForm
    from .models import EmployeeProfile
    from django.contrib import messages
    
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST, request.FILES)
        
        # Check if passwords match
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
                # Create user but don't save yet
                user = form.save(commit=False)
                # Set password
                user.set_password(password)
                user.save()
                
                # Create or get EmployeeProfile for the new user
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
                # If user was created but profile failed, we might want to delete the user
                if 'user' in locals():
                    try:
                        user.delete()
                    except:
                        pass
                return render(request, 'employees/add_employee.html', {'form': form})
        else:
            # Show form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return render(request, 'employees/add_employee.html', {'form': form})
    else:
        form = AddEmployeeForm()
    
    return render(request, 'employees/add_employee.html', {'form': form})
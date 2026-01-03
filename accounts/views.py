# views.py - Add these views to your employees app

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime

@login_required
def dashboard(request):
    """
    Main dashboard view - shows different content based on user role
    """
    user = request.user
    
    # Check if user is admin/staff
    if user.is_staff or user.is_superuser:
        return admin_dashboard(request)
    else:
        return employee_dashboard(request)


@login_required
def admin_dashboard(request):
    """
    Admin dashboard - shows all employees with their attendance status
    """
    # Get all employees (you'll need to adjust this based on your User model)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Get all non-admin users
    all_users = User.objects.filter(is_staff=False, is_superuser=False)
    
    # Prepare employee data with attendance status
    employees = []
    for user in all_users:
        # Get today's attendance record (you'll need to create an Attendance model)
        # For now, we'll use dummy data
        employee_data = {
            'id': user.id,
            'name': f"{user.first_name} {user.last_name}" if user.first_name else user.login_id,
            'email': user.email,
            'job_position': getattr(user, 'job_position', None),
            'department': getattr(user, 'department', None),
            'profile_picture': getattr(user, 'profile_picture', None),
            'attendance_status': 'absent',  # Default
            'check_in_time': None,
        }
        
        # Check if user has checked in today
        # try:
        #     from .models import Attendance
        #     today = timezone.now().date()
        #     attendance = Attendance.objects.filter(
        #         employee=user, 
        #         date=today
        #     ).first()
        #     
        #     if attendance:
        #         if attendance.is_on_leave:
        #             employee_data['attendance_status'] = 'leave'
        #         elif attendance.check_in_time:
        #             employee_data['attendance_status'] = 'present'
        #             employee_data['check_in_time'] = attendance.check_in_time
        # except:
        #     pass
        
        employees.append(employee_data)
    
    context = {
        'employees': employees,
        'total_employees': len(employees),
        'present_count': len([e for e in employees if e['attendance_status'] == 'present']),
        'leave_count': len([e for e in employees if e['attendance_status'] == 'leave']),
        'absent_count': len([e for e in employees if e['attendance_status'] == 'absent']),
    }
    
    return render(request, 'employees/admin_dashboard.html', context)


@login_required
def employee_dashboard(request):
    """
    Employee dashboard - shows personal info and attendance
    """
    user = request.user
    
    # Get employee's attendance data
    # try:
    #     from .models import Attendance
    #     today = timezone.now().date()
    #     today_attendance = Attendance.objects.filter(
    #         employee=user,
    #         date=today
    #     ).first()
    # except:
    #     today_attendance = None
    
    context = {
        'user': user,
        # 'today_attendance': today_attendance,
        # Add more employee-specific data here
    }
    
    return render(request, 'employees/employee_dashboard.html', context)


@login_required
def profile(request):
    """
    User profile view
    """
    user = request.user
    
    # Get salary info if exists
    # try:
    #     from .models import SalaryInfo
    #     salary_info = SalaryInfo.objects.filter(employee=user).first()
    # except:
    #     salary_info = None
    
    context = {
        'user': user,
        # 'salary_info': salary_info,
        # 'components': [],
        # 'pf': None,
        # 'tax_deductions': [],
    }
    
    return render(request, 'employees/profile.html', context)
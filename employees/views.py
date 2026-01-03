from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import EmployeeProfile
from accounts.models import User
from .forms import AddEmployeeForm, EditEmployeeForm


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


@login_required
def employees(request):
    # Get all users (employees)
    all_employees = User.objects.all().order_by('-date_joined')
    
    # Add pagination (10 employees per page)
    paginator = Paginator(all_employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'employees': page_obj,
        'is_admin': request.user.role in ['ADMIN', 'HR']
    }
    
    return render(request, 'employees/employees.html', context)


@login_required
def add_employee(request):
    # Check if user is admin or HR
    if request.user.role not in ['ADMIN', 'HR']:
        messages.error(request, 'You do not have permission to add employees.')
        return redirect('employee:employees')
    
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Employee {user.login_id} has been added successfully!')
            return redirect('employee:employees')
    else:
        form = AddEmployeeForm()
    
    context = {
        'form': form,
        'title': 'Add New Employee'
    }
    return render(request, 'employees/add_employee.html', context)


@login_required
def edit_employee(request, employee_id):
    # Check if user is admin or HR
    if request.user.role not in ['ADMIN', 'HR']:
        messages.error(request, 'You do not have permission to edit employees.')
        return redirect('employee:employees')
    
    employee = get_object_or_404(User, id=employee_id)
    
    if request.method == 'POST':
        form = EditEmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employee {employee.login_id} has been updated successfully!')
            return redirect('employee:employees')
    else:
        form = EditEmployeeForm(instance=employee)
    
    context = {
        'form': form,
        'employee': employee,
        'title': 'Edit Employee'
    }
    return render(request, 'employees/edit_employee.html', context)


@login_required
def delete_employee(request, employee_id):
    # Check if user is admin
    if request.user.role != 'ADMIN':
        messages.error(request, 'You do not have permission to delete employees.')
        return redirect('employee:employees')
    
    employee = get_object_or_404(User, id=employee_id)
    
    # Prevent deleting yourself
    if employee.id == request.user.id:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('employee:employees')
    
    if request.method == 'POST':
        login_id = employee.login_id
        employee.delete()
        messages.success(request, f'Employee {login_id} has been deleted successfully!')
        return redirect('employee:employees')
    
    context = {
        'employee': employee
    }
    return render(request, 'employees/delete_employee.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Attendance


def attendance(request):
    return redirect('attendance:list')


@login_required
def check_in_out_view(request):
    if request.method == "POST":
        user = request.user
        today = timezone.now().date()
        now = timezone.now().time()

        attendance, created = Attendance.objects.get_or_create(
            employee=user,
            date=today,
            defaults={'check_in': now}
        )

        if created:
            user.is_checked_in = True
            user.done_for_day = False
            user.save()

        if not created and not attendance.check_out:
            attendance.check_out = now
            attendance.save()
            user.is_checked_in = False
            user.done_for_day = True
            user.save()

    # FIXED: Changed 'attendace_list_view' to 'list'
    return redirect('attendance:list')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Attendance

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Attendance
from django.contrib.auth import get_user_model
from django.utils import timezone

@login_required
def attendance_list_view(request):
    user = request.user
    
    # 1. Permission-based queryset
    if user.role in ['ADMIN', 'HR']:
        queryset = Attendance.objects.all()
        # Fetch all employees for the dropdown
        employees = get_user_model().objects.all().order_by('email')
    else:
        queryset = Attendance.objects.filter(employee=user)
        employees = None

    # 2. Apply Filters from GET parameters
    selected_date = request.GET.get('date')
    selected_employee = request.GET.get('employee')

    if selected_date:
        queryset = queryset.filter(date=selected_date)
    
    # Only HR/Admin can filter by specific employee
    if selected_employee and user.role in ['ADMIN', 'HR']:
        queryset = queryset.filter(employee_id=selected_employee)

    # 3. Final records and context
    records = queryset.order_by('-date')[:100]
    
    context = {
        'records': records,
        'employees': employees,
        'selected_date': selected_date or timezone.now().date().isoformat(),
        'selected_employee': selected_employee,
    }

    if user.role in ['ADMIN', 'HR']:
        return render(request, 'attendance/list_admin.html', context)
    return render(request, 'attendance/list.html', context)
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


@login_required
def attendance_list_view(request):
    user = request.user
    
    # Filter by role
    if user.role == 'ADMIN' or user.role == 'HR':
        queryset = Attendance.objects.all()
    else:
        queryset = Attendance.objects.filter(employee=user)

    records = queryset.order_by('-date')[:100]
    
    context = {
        'records': records,
    }
    
    if user.role == 'ADMIN' or user.role == 'HR':
        return render(request, 'attendance/list_admin.html', context)
    else:
        return render(request, 'attendance/list.html', context)
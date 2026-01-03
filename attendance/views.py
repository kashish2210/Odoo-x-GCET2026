from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Attendance


# Create your views here.
def attendance(request):
    return render(request, 'attendance/attendance.html')


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

    return redirect('attendance:attendance')
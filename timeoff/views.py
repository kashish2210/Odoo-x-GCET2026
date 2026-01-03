from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Q
from datetime import datetime
from .models import TimeOffRequest, TimeOffType, TimeOffBalance
from .forms import TimeOffRequestForm


@login_required
def timeoff_list(request):
    """Display list of time off requests"""
    user = request.user
    current_year = datetime.now().year
    
    # Admin and Manager can see all requests
    if user.role in ['admin', 'manager']:
        timeoff_requests = TimeOffRequest.objects.all().select_related(
            'employee', 'time_off_type', 'reviewed_by'
        ).order_by('-created_at')
    else:
        # Employees see only their own requests
        timeoff_requests = TimeOffRequest.objects.filter(
            employee=user
        ).select_related('time_off_type', 'reviewed_by').order_by('-created_at')
    
    # Calculate balances for the current user
    paid_time_off_type = TimeOffType.objects.filter(name__icontains='Paid').first()
    sick_leave_type = TimeOffType.objects.filter(name__icontains='Sick').first()
    
    # Get approved time off for current year
    approved_paid = TimeOffRequest.objects.filter(
        employee=user,
        time_off_type=paid_time_off_type,
        status='approved',
        start_date__year=current_year
    ).aggregate(total=Sum('allocation'))['total'] or 0
    
    approved_sick = TimeOffRequest.objects.filter(
        employee=user,
        time_off_type=sick_leave_type,
        status='approved',
        start_date__year=current_year
    ).aggregate(total=Sum('allocation'))['total'] or 0
    
    # Default allocations
    paid_days_total = 26
    sick_days_total = 7
    
    context = {
        'timeoff_requests': timeoff_requests,
        'paid_days_available': paid_days_total - float(approved_paid),
        'sick_days_available': sick_days_total - float(approved_sick),
    }
    return render(request, 'timeoff/timeoff_list.html', context)


@login_required
def request_timeoff(request):
    """Create a new time off request"""
    if request.method == 'POST':
        form = TimeOffRequestForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                timeoff_request = form.save(commit=False)
                timeoff_request.employee = request.user
                
                # Validate allocation doesn't exceed available days
                current_year = datetime.now().year
                approved_requests = TimeOffRequest.objects.filter(
                    employee=request.user,
                    time_off_type=timeoff_request.time_off_type,
                    status='approved',
                    start_date__year=current_year
                ).aggregate(total=Sum('allocation'))['total'] or 0
                
                # Determine max days based on type
                if 'Paid' in timeoff_request.time_off_type.name:
                    max_days = 26
                elif 'Sick' in timeoff_request.time_off_type.name:
                    max_days = 7
                else:
                    max_days = 365  # No limit for unpaid
                
                if float(approved_requests) + float(timeoff_request.allocation) > max_days:
                    messages.error(request, f'Insufficient balance. You have {max_days - float(approved_requests)} days available.')
                    return render(request, 'timeoff/timeoff_request.html', {
                        'form': form,
                        'timeoff_types': TimeOffType.objects.filter(is_active=True),
                    })
                
                timeoff_request.save()
                
                messages.success(request, 'Time off request submitted successfully! Awaiting approval.')
                return redirect('timeoff:timeoff_list')
            except Exception as e:
                messages.error(request, f'Error submitting request: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = TimeOffRequestForm()
    
    # Get available time off types
    timeoff_types = TimeOffType.objects.filter(is_active=True)
    
    context = {
        'form': form,
        'timeoff_types': timeoff_types,
    }
    return render(request, 'timeoff/timeoff_request.html', context)


@login_required
def approve_timeoff(request, request_id):
    """Approve a time off request (Admin/Manager only)"""
    if request.user.role not in ['admin', 'manager']:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        timeoff_request = get_object_or_404(TimeOffRequest, id=request_id)
        
        if timeoff_request.status != 'pending':
            return JsonResponse({'success': False, 'error': 'Request already processed'})
        
        timeoff_request.status = 'approved'
        timeoff_request.reviewed_by = request.user
        timeoff_request.reviewed_at = timezone.now()
        timeoff_request.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def reject_timeoff(request, request_id):
    """Reject a time off request (Admin/Manager only)"""
    if request.user.role not in ['admin', 'manager']:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        timeoff_request = get_object_or_404(TimeOffRequest, id=request_id)
        
        if timeoff_request.status != 'pending':
            return JsonResponse({'success': False, 'error': 'Request already processed'})
        
        timeoff_request.status = 'rejected'
        timeoff_request.reviewed_by = request.user
        timeoff_request.reviewed_at = timezone.now()
        timeoff_request.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def timeoff_detail(request, request_id):
    """View detailed information about a time off request"""
    timeoff_request = get_object_or_404(TimeOffRequest, id=request_id)
    
    # Check permissions
    if request.user.role not in ['admin', 'manager'] and timeoff_request.employee != request.user:
        messages.error(request, 'You do not have permission to view this request')
        return redirect('timeoff:timeoff_list')
    
    context = {
        'timeoff_request': timeoff_request,
    }
    return render(request, 'timeoff/timeoff_detail.html', context)
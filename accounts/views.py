from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    """Dashboard view - only accessible to logged in users"""
    context = {
        'user': request.user
    }
    return render(request, 'dashboard.html', context)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    """Dashboard view - only accessible to logged in users"""
    return render(request, 'dashboard.html')


@login_required
def profile(request):
    """Profile view - only accessible to logged in users"""
    return render(request, 'profile.html')
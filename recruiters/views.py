from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def recruiter_dashboard(request):
    return render(request, "recruiters/dashboard.html")
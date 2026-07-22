from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def student_dashboard(request):
    return render(request, "students/dashboard.html")

def student_profile(request):
    return render(request, "students/profile.html")

def login_view(request):
    return render(request, "accounts/login.html")
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def recruiter_dashboard(request):

    return render(
        request,
        "recruiters/dashboard.html",
    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def placement_dashboard(request):

    return render(
        request,
        "placement/dashboard.html",
    )
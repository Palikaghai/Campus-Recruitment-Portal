from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def placement_dashboard(request):
    return render(request, "placement/dashboard.html")
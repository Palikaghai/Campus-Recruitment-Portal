from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import StudentProfile
from placement.models import PlacementDrive, Application
from placement.models import PlacementDrive

from placement.models import Application


@login_required
def student_dashboard(request):

    student = get_object_or_404(StudentProfile, user=request.user)

    drives = PlacementDrive.objects.filter(
        is_active=True
    ).order_by("-created_at")

    applications = Application.objects.filter(student=student)

    applied_drive_ids = applications.values_list(
        "drive_id",
        flat=True
    )

    context = {
        "student": student,
        "drives": drives,
        "applications": applications,
        "applied_drive_ids": applied_drive_ids,
        "total_drives": drives.count(),
        "total_applications": applications.count(),
    }

    return render(
        request,
        "students/dashboard.html",
        context,
    )


@login_required
def apply_drive(request, drive_id):

    student = get_object_or_404(StudentProfile, user=request.user)

    drive = get_object_or_404(
        PlacementDrive,
        id=drive_id,
        is_active=True
    )

    application, created = Application.objects.get_or_create(
        student=student,
        drive=drive
    )

    if created:
        messages.success(
            request,
            "Application submitted successfully!"
        )
    else:
        messages.warning(
            request,
            "You have already applied for this drive."
        )

    return redirect("student_dashboard")
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StudentProfile

@login_required
def student_profile(request):

    profile = StudentProfile.objects.get(user=request.user)

    context = {
        "profile": profile,
    }

    return render(
        request,
        "students/profile.html",
        context,
    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import StudentProfile

@login_required
def student_resume(request):

    profile = StudentProfile.objects.get(user=request.user)

    if request.method == "POST":

        if request.FILES.get("resume"):

            profile.resume = request.FILES["resume"]
            profile.save()

            return redirect("student_resume")

    return render(
        request,
        "students/resume.html",
        {
            "profile": profile
        }
    )
@login_required
def placement_drives(request):

    drives = PlacementDrive.objects.filter(
        is_active=True
    ).select_related("company")

    return render(
        request,
        "students/placement_drives.html",
        {
            "drives": drives,
        },
    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from students.models import StudentProfile

@login_required
def student_applications(request):

    profile = StudentProfile.objects.get(user=request.user)

    applications = (
        Application.objects
        .filter(student=profile)
        .select_related("drive", "drive__company")
        .order_by("-applied_on")
    )

    return render(
        request,
        "students/applications.html",
        {
            "applications": applications,
        },
    )
from interviews.models import Interview

@login_required
def student_interviews(request):

    interviews = (
        Interview.objects
        .filter(application__student__user=request.user)
        .select_related(
            "application",
            "application__drive",
            "application__drive__company"
        )
    )

    return render(
        request,
        "students/interviews.html",
        {
            "interviews": interviews
        }
    )
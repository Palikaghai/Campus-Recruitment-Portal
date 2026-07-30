from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import StudentProfile
from placement.models import PlacementDrive, Application
from interviews.models import Interview
from core.models import notify_user


@login_required
def student_dashboard(request):
    student, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "registration_number": f"REG-{request.user.id:04d}",
            "department": "Computer Science",
            "batch": 2026,
            "cgpa": 8.00,
        }
    )

    drives = PlacementDrive.objects.filter(is_active=True).select_related("company").order_by("-created_at")
    applications = Application.objects.filter(student=student).select_related("drive", "drive__company")
    applied_drive_ids = applications.values_list("drive_id", flat=True)
    interviews = Interview.objects.filter(application__student=student)

    context = {
        "student": student,
        "drives": drives,
        "applications": applications,
        "applied_drive_ids": applied_drive_ids,
        "interviews_count": interviews.count(),
        "total_drives": drives.count(),
        "total_applications": applications.count(),
        "completion_percentage": student.profile_completion_percentage,
    }
    return render(request, "students/dashboard.html", context)


@login_required
def apply_drive(request, drive_id):
    student = get_object_or_404(StudentProfile, user=request.user)
    drive = get_object_or_404(PlacementDrive, id=drive_id, is_active=True)

    if student.cgpa < drive.eligibility_cgpa:
        messages.error(request, f"Sorry, your CGPA ({student.cgpa}) does not meet the eligibility cutoff ({drive.eligibility_cgpa}) for this drive.")
        return redirect("student_dashboard")

    application, created = Application.objects.get_or_create(student=student, drive=drive)

    if created:
        messages.success(request, f"Application for '{drive.job_role}' at {drive.company.name} submitted successfully!")
        
        # Notify Recruiter if linked
        if drive.recruiter and drive.recruiter.user:
            notify_user(
                user=drive.recruiter.user,
                title="New Applicant!",
                message=f"{request.user.get_full_name()} applied for your drive '{drive.job_role}'.",
                notification_type="info",
                link=f"/recruiter/drives/{drive.id}/applicants/"
            )
    else:
        messages.warning(request, "You have already applied for this placement drive.")

    return redirect("student_dashboard")


@login_required
def student_profile(request):
    profile, _ = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={"registration_number": f"REG-{request.user.id:04d}", "department": "Computer Science", "batch": 2026, "cgpa": 8.0}
    )

    if request.method == "POST":
        profile.registration_number = request.POST.get("registration_number", profile.registration_number)
        profile.department = request.POST.get("department", profile.department)
        profile.batch = request.POST.get("batch", profile.batch)
        profile.cgpa = request.POST.get("cgpa", profile.cgpa)
        profile.skills = request.POST.get("skills", profile.skills)
        profile.projects = request.POST.get("projects", profile.projects)
        profile.certifications = request.POST.get("certifications", profile.certifications)
        profile.bio = request.POST.get("bio", profile.bio)

        if request.FILES.get("resume"):
            profile.resume = request.FILES["resume"]

        profile.save()

        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("student_profile")

    context = {
        "profile": profile,
        "completion_percentage": profile.profile_completion_percentage,
    }
    return render(request, "students/profile.html", context)


@login_required
def student_resume(request):
    profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == "POST":
        if request.FILES.get("resume"):
            profile.resume = request.FILES["resume"]
            profile.save()
            messages.success(request, "Resume uploaded successfully!")
            return redirect("student_resume")

    return render(request, "students/resume.html", {"profile": profile})


@login_required
def placement_drives(request):
    drives = PlacementDrive.objects.filter(is_active=True).select_related("company").order_by("-created_at")
    student = StudentProfile.objects.filter(user=request.user).first()
    applied_drive_ids = Application.objects.filter(student=student).values_list("drive_id", flat=True) if student else []

    search_query = request.GET.get("search", "")
    if search_query:
        drives = drives.filter(job_role__icontains=search_query) | drives.filter(company__name__icontains=search_query)

    return render(
        request,
        "students/placement_drives.html",
        {
            "drives": drives,
            "applied_drive_ids": applied_drive_ids,
            "search_query": search_query,
        }
    )


@login_required
def drive_detail(request, drive_id):
    drive = get_object_or_404(PlacementDrive, id=drive_id, is_active=True)
    student = StudentProfile.objects.filter(user=request.user).first()

    already_applied = False
    is_eligible = True

    if student:
        already_applied = Application.objects.filter(student=student, drive=drive).exists()
        is_eligible = student.cgpa >= drive.eligibility_cgpa

    # Count total applicants for social proof
    total_applicants = Application.objects.filter(drive=drive).count()

    context = {
        "drive": drive,
        "student": student,
        "already_applied": already_applied,
        "is_eligible": is_eligible,
        "total_applicants": total_applicants,
    }
    return render(request, "students/drive_detail.html", context)


@login_required
def student_applications(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    applications = Application.objects.filter(student=profile).select_related("drive", "drive__company").order_by("-applied_on")

    return render(request, "students/applications.html", {"applications": applications})


@login_required
def student_interviews(request):
    interviews = Interview.objects.filter(application__student__user=request.user).select_related(
        "application", "application__drive", "application__drive__company"
    ).order_by("-interview_date")

    return render(request, "students/interviews.html", {"interviews": interviews})
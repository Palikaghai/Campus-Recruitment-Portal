from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from .models import RecruiterProfile
from .forms import CompanyForm, PlacementDriveForm, InterviewScheduleForm
from placement.models import Company, PlacementDrive, Application
from interviews.models import Interview
from core.models import notify_user
from accounts.models import CustomUser


def _get_recruiter_profile(user):
    profile, created = RecruiterProfile.objects.get_or_create(
        user=user,
        defaults={"company_name": user.first_name or "Company", "designation": "Recruiter"}
    )
    return profile


@login_required
def recruiter_dashboard(request):
    recruiter = _get_recruiter_profile(request.user)
    company = Company.objects.filter(recruiter=recruiter).first()
    
    if not company:
        company = Company.objects.filter(name__iexact=recruiter.company_name).first()
        if company:
            company.recruiter = recruiter
            company.save()

    drives = PlacementDrive.objects.filter(Q(recruiter=recruiter) | Q(company=company) if company else Q(recruiter=recruiter))
    
    total_drives = drives.count()
    active_drives = drives.filter(is_active=True).count()
    
    applications = Application.objects.filter(drive__in=drives)
    total_applications = applications.count()
    
    interviews_scheduled = Interview.objects.filter(application__drive__in=drives).count()
    selected_students = applications.filter(status="Selected").count()
    
    recent_applications = applications.select_related("student__user", "drive").order_by("-applied_on")[:6]
    
    context = {
        "recruiter": recruiter,
        "company": company,
        "total_drives": total_drives,
        "active_drives": active_drives,
        "total_applications": total_applications,
        "interviews_scheduled": interviews_scheduled,
        "selected_students": selected_students,
        "recent_applications": recent_applications,
    }
    return render(request, "recruiters/dashboard.html", context)


@login_required
def company_profile(request):
    recruiter = _get_recruiter_profile(request.user)
    company = Company.objects.filter(recruiter=recruiter).first()
    
    if not company:
        company = Company.objects.filter(name__iexact=recruiter.company_name).first()
        if company:
            company.recruiter = recruiter
            company.save()

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            company_obj = form.save(commit=False)
            company_obj.recruiter = recruiter
            company_obj.save()
            
            recruiter.company_name = company_obj.name
            if company_obj.website:
                recruiter.company_website = company_obj.website
            recruiter.save()
            
            messages.success(request, "Company profile updated successfully!")
            return redirect("recruiter_company_profile")
    else:
        form = CompanyForm(instance=company, initial={"name": recruiter.company_name, "website": recruiter.company_website})

    return render(request, "recruiters/company_profile.html", {"form": form, "company": company, "recruiter": recruiter})


@login_required
def create_drive(request):
    recruiter = _get_recruiter_profile(request.user)
    company = Company.objects.filter(recruiter=recruiter).first()

    if not company:
        messages.warning(request, "Please set up your Company Profile first before creating a Placement Drive.")
        return redirect("recruiter_company_profile")

    if request.method == "POST":
        form = PlacementDriveForm(request.POST)
        if form.is_valid():
            drive = form.save(commit=False)
            drive.company = company
            drive.recruiter = recruiter
            drive.save()

            # Notify placement officers
            officers = CustomUser.objects.filter(role="placement_officer")
            for officer in officers:
                notify_user(
                    user=officer,
                    title="New Drive Posted",
                    message=f"{company.name} posted a new drive for {drive.job_role}.",
                    notification_type="info",
                    link="/placement/drives/"
                )

            messages.success(request, f"Placement Drive for '{drive.job_role}' created successfully!")
            return redirect("recruiter_manage_drives")
    else:
        form = PlacementDriveForm(initial={"company": company})

    return render(request, "recruiters/drive_form.html", {"form": form, "company": company, "title": "Create Placement Drive"})


@login_required
def edit_drive(request, drive_id):
    recruiter = _get_recruiter_profile(request.user)
    drive = get_object_or_404(PlacementDrive, id=drive_id, recruiter=recruiter)

    if request.method == "POST":
        form = PlacementDriveForm(request.POST, instance=drive)
        if form.is_valid():
            form.save()
            messages.success(request, f"Placement Drive '{drive.job_role}' updated successfully!")
            return redirect("recruiter_manage_drives")
    else:
        form = PlacementDriveForm(instance=drive)

    return render(request, "recruiters/drive_form.html", {"form": form, "drive": drive, "title": f"Edit {drive.job_role}"})


@login_required
def delete_drive(request, drive_id):
    recruiter = _get_recruiter_profile(request.user)
    drive = get_object_or_404(PlacementDrive, id=drive_id, recruiter=recruiter)
    
    if request.method == "POST":
        role_name = drive.job_role
        drive.delete()
        messages.success(request, f"Drive '{role_name}' deleted successfully.")
        return redirect("recruiter_manage_drives")

    return render(request, "recruiters/confirm_delete_drive.html", {"drive": drive})


@login_required
def manage_drives(request):
    recruiter = _get_recruiter_profile(request.user)
    drives = PlacementDrive.objects.filter(recruiter=recruiter).annotate(app_count=Count("application")).order_by("-created_at")

    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")

    if search_query:
        drives = drives.filter(Q(job_role__icontains=search_query) | Q(location__icontains=search_query))
    if status_filter == "active":
        drives = drives.filter(is_active=True)
    elif status_filter == "inactive":
        drives = drives.filter(is_active=False)

    context = {
        "drives": drives,
        "search_query": search_query,
        "status_filter": status_filter,
    }
    return render(request, "recruiters/manage_drives.html", context)


@login_required
def drive_applicants(request, drive_id):
    recruiter = _get_recruiter_profile(request.user)
    drive = get_object_or_404(PlacementDrive, id=drive_id, recruiter=recruiter)
    applications = Application.objects.filter(drive=drive).select_related("student__user", "interview").order_by("-applied_on")

    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")

    if search_query:
        applications = applications.filter(
            Q(student__user__first_name__icontains=search_query) |
            Q(student__user__last_name__icontains=search_query) |
            Q(student__registration_number__icontains=search_query) |
            Q(student__skills__icontains=search_query)
        )
    if status_filter:
        applications = applications.filter(status=status_filter)

    context = {
        "drive": drive,
        "applications": applications,
        "search_query": search_query,
        "status_filter": status_filter,
        "status_choices": Application.STATUS,
    }
    return render(request, "recruiters/applicants.html", context)


@login_required
def schedule_interview(request, application_id):
    recruiter = _get_recruiter_profile(request.user)
    application = get_object_or_404(Application, id=application_id, drive__recruiter=recruiter)
    
    interview = getattr(application, "interview", None)

    if request.method == "POST":
        form = InterviewScheduleForm(request.POST, instance=interview)
        if form.is_valid():
            interview_obj = form.save(commit=False)
            interview_obj.application = application
            interview_obj.save()

            application.status = "Interview"
            application.save()

            # Notify Student
            notify_user(
                user=application.student.user,
                title="Interview Scheduled! 📅",
                message=f"Your interview for {application.drive.job_role} at {application.drive.company.name} has been scheduled for {interview_obj.interview_date} at {interview_obj.interview_time}.",
                notification_type="info",
                link="/student/interviews/"
            )

            messages.success(request, f"Interview scheduled for {application.student.user.get_full_name()}!")
            return redirect("recruiter_drive_applicants", drive_id=application.drive.id)
    else:
        form = InterviewScheduleForm(instance=interview)

    return render(
        request,
        "recruiters/schedule_interview.html",
        {"form": form, "application": application, "interview": interview}
    )


@login_required
def update_applicant_status(request, application_id, new_status):
    recruiter = _get_recruiter_profile(request.user)
    application = get_object_or_404(Application, id=application_id, drive__recruiter=recruiter)

    valid_statuses = dict(Application.STATUS)
    if new_status in valid_statuses:
        application.status = new_status
        application.save()

        # Send notification to student
        if new_status == "Shortlisted":
            notify_user(
                user=application.student.user,
                title="Application Shortlisted! 🎉",
                message=f"You have been shortlisted for {application.drive.job_role} at {application.drive.company.name}.",
                notification_type="success",
                link="/student/applications/"
            )
        elif new_status == "Selected":
            notify_user(
                user=application.student.user,
                title="Congratulations! Offer Received 🌟",
                message=f"You have been SELECTED for {application.drive.job_role} at {application.drive.company.name}!",
                notification_type="success",
                link="/student/applications/"
            )
        elif new_status == "Rejected":
            notify_user(
                user=application.student.user,
                title="Application Update",
                message=f"Your application status for {application.drive.job_role} at {application.drive.company.name} has been updated to Rejected.",
                notification_type="danger",
                link="/student/applications/"
            )

        messages.success(request, f"Status updated to '{new_status}' for {application.student.user.get_full_name()}.")
    
    return redirect("recruiter_drive_applicants", drive_id=application.drive.id)
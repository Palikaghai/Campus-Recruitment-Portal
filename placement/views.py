from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from students.models import StudentProfile
from recruiters.models import RecruiterProfile
from placement.models import Company, PlacementDrive, Application, PlacementOfficerProfile
from .forms import StudentEditForm, AddRecruiterForm, CompanyApprovalForm
from accounts.models import CustomUser
from core.models import notify_user


def _get_officer_profile(user):
    profile, created = PlacementOfficerProfile.objects.get_or_create(
        user=user,
        defaults={"employee_id": f"EMP-{user.id:04d}", "department": "Training & Placement"}
    )
    return profile


@login_required
def placement_dashboard(request):
    officer = _get_officer_profile(request.user)

    total_students = StudentProfile.objects.count()
    total_recruiters = RecruiterProfile.objects.count()
    total_drives = PlacementDrive.objects.count()
    
    placed_applications = Application.objects.filter(status="Selected")
    total_offers = placed_applications.count()
    
    unique_placed_students = placed_applications.values("student").distinct().count()
    placement_rate = round((unique_placed_students / total_students * 100), 1) if total_students > 0 else 0.0

    recent_drives = PlacementDrive.objects.select_related("company").order_by("-created_at")[:5]
    recent_placements = placed_applications.select_related("student__user", "drive__company").order_by("-applied_on")[:5]

    context = {
        "officer": officer,
        "total_students": total_students,
        "total_recruiters": total_recruiters,
        "total_drives": total_drives,
        "total_offers": total_offers,
        "placement_rate": placement_rate,
        "recent_drives": recent_drives,
        "recent_placements": recent_placements,
    }
    return render(request, "placement/dashboard.html", context)


@login_required
def manage_students(request):
    students = StudentProfile.objects.select_related("user").annotate(
        app_count=Count("application"),
        is_placed=Count("application", filter=Q(application__status="Selected"))
    ).order_by("-id")

    search_query = request.GET.get("search", "")
    dept_filter = request.GET.get("department", "")

    if search_query:
        students = students.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(registration_number__icontains=search_query)
        )
    if dept_filter:
        students = students.filter(department__iexact=dept_filter)

    departments = StudentProfile.objects.values_list("department", flat=True).distinct()

    context = {
        "students": students,
        "search_query": search_query,
        "dept_filter": dept_filter,
        "departments": departments,
    }
    return render(request, "placement/students.html", context)


@login_required
def edit_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    user = student.user

    if request.method == "POST":
        form = StudentEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()
            form.save()
            messages.success(request, f"Student profile for {user.get_full_name()} updated successfully.")
            return redirect("placement_manage_students")
    else:
        form = StudentEditForm(
            instance=student,
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
        )

    return render(request, "placement/edit_student.html", {"form": form, "student": student})


@login_required
def toggle_student_active(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    student.user.is_active = not student.user.is_active
    student.user.save()
    status_str = "activated" if student.user.is_active else "deactivated"
    messages.success(request, f"Student {student.user.get_full_name()} has been {status_str}.")
    return redirect("placement_manage_students")


@login_required
def delete_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    user = student.user
    if request.method == "POST":
        user.delete()
        messages.success(request, "Student account deleted successfully.")
        return redirect("placement_manage_students")
    return render(request, "placement/confirm_delete_student.html", {"student": student})


@login_required
def manage_recruiters(request):
    recruiters = RecruiterProfile.objects.select_related("user").order_by("-id")
    companies = Company.objects.select_related("recruiter").order_by("-id")

    search_query = request.GET.get("search", "")
    if search_query:
        recruiters = recruiters.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(company_name__icontains=search_query)
        )
        companies = companies.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    context = {
        "recruiters": recruiters,
        "companies": companies,
        "search_query": search_query,
    }
    return render(request, "placement/recruiters.html", context)


@login_required
def add_recruiter(request):
    if request.method == "POST":
        form = AddRecruiterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists.")
            else:
                user = CustomUser.objects.create_user(
                    username=email,
                    email=email,
                    password=form.cleaned_data["password"],
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    role="recruiter"
                )
                recruiter = RecruiterProfile.objects.create(
                    user=user,
                    company_name=form.cleaned_data["company_name"],
                    designation=form.cleaned_data["designation"],
                    company_website=form.cleaned_data.get("company_website", "")
                )
                company, created = Company.objects.get_or_create(
                    name=form.cleaned_data["company_name"],
                    defaults={
                        "website": form.cleaned_data.get("company_website", ""),
                        "email": email,
                        "location": "Main Office",
                        "recruiter": recruiter,
                        "is_approved": True,
                    }
                )
                if not created:
                    company.recruiter = recruiter
                    company.is_approved = True
                    company.save()

                messages.success(request, f"Recruiter {user.get_full_name()} added successfully!")
                return redirect("placement_manage_recruiters")
    else:
        form = AddRecruiterForm()

    return render(request, "placement/add_recruiter.html", {"form": form})


@login_required
def toggle_company_approval(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.is_approved = not company.is_approved
    company.save()
    status_str = "Approved" if company.is_approved else "Unapproved"
    messages.success(request, f"Company '{company.name}' marked as {status_str}.")
    return redirect("placement_manage_recruiters")


@login_required
def delete_recruiter(request, recruiter_id):
    recruiter = get_object_or_404(RecruiterProfile, id=recruiter_id)
    user = recruiter.user
    if request.method == "POST":
        user.delete()
        messages.success(request, "Recruiter deleted successfully.")
        return redirect("placement_manage_recruiters")
    return render(request, "placement/confirm_delete_recruiter.html", {"recruiter": recruiter})


@login_required
def manage_officer_drives(request):
    drives = PlacementDrive.objects.select_related("company", "recruiter", "created_by").annotate(app_count=Count("application")).order_by("-created_at")

    search_query = request.GET.get("search", "")
    if search_query:
        drives = drives.filter(
            Q(job_role__icontains=search_query) |
            Q(company__name__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    context = {
        "drives": drives,
        "search_query": search_query,
    }
    return render(request, "placement/drives.html", context)


@login_required
def toggle_drive_active(request, drive_id):
    drive = get_object_or_404(PlacementDrive, id=drive_id)
    drive.is_active = not drive.is_active
    drive.save()
    status_str = "Activated" if drive.is_active else "Deactivated"
    messages.success(request, f"Drive for {drive.job_role} at {drive.company.name} {status_str}.")
    return redirect("placement_manage_drives")


@login_required
def delete_officer_drive(request, drive_id):
    drive = get_object_or_404(PlacementDrive, id=drive_id)
    if request.method == "POST":
        role_name = drive.job_role
        drive.delete()
        messages.success(request, f"Drive '{role_name}' deleted successfully.")
        return redirect("placement_manage_drives")
    return render(request, "placement/confirm_delete_drive.html", {"drive": drive})


@login_required
def placement_reports(request):
    total_students = StudentProfile.objects.count()
    placed_students_count = Application.objects.filter(status="Selected").values("student").distinct().count()
    unplaced_students_count = max(0, total_students - placed_students_count)
    in_process_count = Application.objects.filter(status__in=["Applied", "Shortlisted", "Interview"]).values("student").distinct().count()

    # Company-wise hiring count
    company_hiring = (
        Application.objects.filter(status="Selected")
        .values("drive__company__name")
        .annotate(count=Count("id"))
        .order_by("-count")[:8]
    )
    company_names = [item["drive__company__name"] for item in company_hiring]
    company_counts = [item["count"] for item in company_hiring]

    # Branch-wise placement
    branch_hiring = (
        Application.objects.filter(status="Selected")
        .values("student__department")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    branch_names = [item["student__department"] or "General" for item in branch_hiring]
    branch_counts = [item["count"] for item in branch_hiring]

    # Monthly placement trend
    monthly_trend = (
        Application.objects.filter(status="Selected")
        .annotate(month=TruncMonth("applied_on"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")[:6]
    )
    month_labels = [item["month"].strftime("%b %Y") if item["month"] else "Recent" for item in monthly_trend]
    month_counts = [item["count"] for item in monthly_trend]

    context = {
        "total_students": total_students,
        "placed_students": placed_students_count,
        "unplaced_students": unplaced_students_count,
        "in_process_students": in_process_count,
        "company_names": company_names,
        "company_counts": company_counts,
        "branch_names": branch_names,
        "branch_counts": branch_counts,
        "month_labels": month_labels,
        "month_counts": month_counts,
    }
    return render(request, "placement/reports.html", context)
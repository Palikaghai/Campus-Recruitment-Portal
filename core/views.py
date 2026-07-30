from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from placement.models import PlacementDrive, Company
from students.models import StudentProfile
from core.models import Notification


def home(request):
    featured_drives = PlacementDrive.objects.filter(is_active=True).select_related("company").order_by("-created_at")[:6]
    top_companies = Company.objects.filter(is_approved=True)[:6]
    total_drives = PlacementDrive.objects.filter(is_active=True).count()
    total_companies = Company.objects.count()
    total_students = StudentProfile.objects.count()

    context = {
        "featured_drives": featured_drives,
        "top_companies": top_companies,
        "total_drives": total_drives,
        "total_companies": total_companies,
        "total_students": total_students,
    }
    return render(request, "home.html", context)


@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user)
    if request.GET.get("mark_all_read") == "1":
        notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, "All notifications marked as read.")
        return redirect("notifications_list")

    context = {
        "notifications": notifications,
    }
    return render(request, "notifications/list.html", context)


@login_required
def mark_notification_read(request, notification_id):
    notif = get_object_or_404(Notification, id=notification_id, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect("notifications_list")


@login_required
def global_search(request):
    query = request.GET.get("q", "").strip()
    drives = PlacementDrive.objects.none()
    companies = Company.objects.none()
    students = StudentProfile.objects.none()

    if query:
        drives = PlacementDrive.objects.filter(
            Q(job_role__icontains=query) |
            Q(company__name__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query),
            is_active=True
        ).select_related("company")

        companies = Company.objects.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query),
            is_approved=True
        )

        if request.user.role in ["recruiter", "placement_officer"]:
            students = StudentProfile.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(registration_number__icontains=query) |
                Q(skills__icontains=query) |
                Q(department__icontains=query)
            ).select_related("user")

    context = {
        "query": query,
        "drives": drives,
        "companies": companies,
        "students": students,
    }
    return render(request, "search_results.html", context)


@login_required
def user_settings(request):
    if request.method == "POST":
        if "update_email" in request.POST:
            new_email = request.POST.get("email", "").strip()
            if new_email and new_email != request.user.email:
                request.user.email = new_email
                request.user.save()
                messages.success(request, "Email address updated successfully!")
            return redirect("user_settings")

        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password was changed successfully!")
                return redirect("user_settings")
            else:
                messages.error(request, "Please correct the errors in the password form.")
    else:
        password_form = PasswordChangeForm(request.user)

    return render(request, "settings.html", {"password_form": password_form})
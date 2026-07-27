import uuid

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .forms import (
    LoginForm,
    StudentRegistrationForm,
    RecruiterRegistrationForm,
    OfficerRegistrationForm,
)

from students.models import StudentProfile
from recruiters.models import RecruiterProfile
from placement.models import PlacementOfficerProfile


def login_view(request):

    if request.user.is_authenticated:

        if request.user.role == "student":
            return redirect("student_dashboard")

        elif request.user.role == "recruiter":
            return redirect("recruiter_dashboard")

        elif request.user.role == "placement_officer":
            return redirect("placement_dashboard")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(request, "Login Successful!")

            if user.role == "student":
                return redirect("student_dashboard")

            elif user.role == "recruiter":
                return redirect("recruiter_dashboard")

            elif user.role == "placement_officer":
                return redirect("placement_dashboard")

        else:
            messages.error(request, "Invalid email or password.")

    return render(
        request,
        "accounts/login.html",
        {"form": form},
    )


def register(request):
    return render(request, "accounts/choose_role.html")


def student_register(request):

    if request.method == "POST":

        form = StudentRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            StudentProfile.objects.create(
                user=user,
                registration_number=f"TEMP-{uuid.uuid4().hex[:8].upper()}",
                department="Not Updated",
                batch=2027,
                cgpa=0.00,
            )

            messages.success(request, "Registration Successful!")
            return redirect("login")

        else:
            print(form.errors)

    else:
        form = StudentRegistrationForm()

    return render(
        request,
        "accounts/student_register.html",
        {"form": form},
    )


def recruiter_register(request):

    if request.method == "POST":

        form = RecruiterRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            RecruiterProfile.objects.create(
                user=user,
                company_name=form.cleaned_data["company_name"],
                designation=form.cleaned_data["designation"],
            )

            messages.success(
                request,
                "Recruiter Registered Successfully!",
            )

            return redirect("login")

    else:
        form = RecruiterRegistrationForm()

    return render(
        request,
        "accounts/recruiter_register.html",
        {"form": form},
    )


def officer_register(request):

    if request.method == "POST":

        form = OfficerRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            PlacementOfficerProfile.objects.create(
                user=user,
                employee_id=form.cleaned_data["employee_id"],
                department=form.cleaned_data["department"],
            )

            messages.success(
                request,
                "Placement Officer Registered Successfully!",
            )

            return redirect("login")

    else:
        form = OfficerRegistrationForm()

    return render(
        request,
        "accounts/officer_register.html",
        {"form": form},
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully.",
    )

    return redirect("login")
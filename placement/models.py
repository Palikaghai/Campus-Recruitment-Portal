from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from students.models import StudentProfile


# ==========================
# Placement Officer Profile
# ==========================

class PlacementOfficerProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    office_phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.get_full_name()


# ==========================
# Company
# ==========================

class Company(models.Model):

    name = models.CharField(max_length=150)

    website = models.URLField(blank=True)

    email = models.EmailField(blank=True)

    description = models.TextField(blank=True)

    location = models.CharField(max_length=100)

    logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# ==========================
# Placement Drive
# ==========================

class PlacementDrive(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="drives"
    )

    job_role = models.CharField(max_length=150)

    package = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    location = models.CharField(max_length=100)

    eligibility_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    description = models.TextField()

    deadline = models.DateField()

    created_by = models.ForeignKey(
        PlacementOfficerProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.company.name} - {self.job_role}"


# ==========================
# Student Application
# ==========================

class Application(models.Model):

    STATUS = (
        ("Applied", "Applied"),
        ("Shortlisted", "Shortlisted"),
        ("Interview", "Interview"),
        ("Selected", "Selected"),
        ("Rejected", "Rejected"),
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    drive = models.ForeignKey(
        PlacementDrive,
        on_delete=models.CASCADE
    )

    applied_on = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Applied"
    )

    class Meta:
        unique_together = ("student", "drive")

    def __str__(self):
        return f"{self.student.user.first_name} -> {self.drive.company.name}"
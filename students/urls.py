from django.urls import path
from . import views

urlpatterns = [
    path(
        "dashboard/",
        views.student_dashboard,
        name="student_dashboard",
    ),

    path(
        "apply/<int:drive_id>/",
        views.apply_drive,
        name="apply_drive",
    ),
    path("profile/", views.student_profile, name="student_profile"),
    path("resume/", views.student_resume, name="student_resume"),
    path(
    "placement-drives/",
    views.placement_drives,
    name="placement_drives",
),
path(
    "applications/",
    views.student_applications,
    name="student_applications",
),
path(
    "interviews/",
    views.student_interviews,
    name="student_interviews",
),
]



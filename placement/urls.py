from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.placement_dashboard, name="placement_dashboard"),
    path("students/", views.manage_students, name="placement_manage_students"),
    path("students/<int:student_id>/edit/", views.edit_student, name="placement_edit_student"),
    path("students/<int:student_id>/toggle-active/", views.toggle_student_active, name="placement_toggle_student_active"),
    path("students/<int:student_id>/delete/", views.delete_student, name="placement_delete_student"),
    
    path("recruiters/", views.manage_recruiters, name="placement_manage_recruiters"),
    path("recruiters/add/", views.add_recruiter, name="placement_add_recruiter"),
    path("recruiters/<int:recruiter_id>/delete/", views.delete_recruiter, name="placement_delete_recruiter"),
    path("companies/<int:company_id>/toggle-approval/", views.toggle_company_approval, name="placement_toggle_company_approval"),
    
    path("drives/", views.manage_officer_drives, name="placement_manage_drives"),
    path("drives/<int:drive_id>/toggle-active/", views.toggle_drive_active, name="placement_toggle_drive_active"),
    path("drives/<int:drive_id>/delete/", views.delete_officer_drive, name="placement_delete_drive"),
    
    path("reports/", views.placement_reports, name="placement_reports"),
]
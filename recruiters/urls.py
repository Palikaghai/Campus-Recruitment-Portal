from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.recruiter_dashboard, name="recruiter_dashboard"),
    path("company/", views.company_profile, name="recruiter_company_profile"),
    path("drives/", views.manage_drives, name="recruiter_manage_drives"),
    path("drives/create/", views.create_drive, name="recruiter_create_drive"),
    path("drives/<int:drive_id>/edit/", views.edit_drive, name="recruiter_edit_drive"),
    path("drives/<int:drive_id>/delete/", views.delete_drive, name="recruiter_delete_drive"),
    path("drives/<int:drive_id>/applicants/", views.drive_applicants, name="recruiter_drive_applicants"),
    path("applicants/<int:application_id>/schedule-interview/", views.schedule_interview, name="recruiter_schedule_interview"),
    path("applicants/<int:application_id>/status/<str:new_status>/", views.update_applicant_status, name="recruiter_update_status"),
]
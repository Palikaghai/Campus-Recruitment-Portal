from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("register/", views.register, name="register"),

    path("register/student/", views.student_register, name="student_register"),

    path("register/recruiter/", views.recruiter_register, name="recruiter_register"),

    path("register/officer/", views.officer_register, name="officer_register"),
]